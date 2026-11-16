
import os
import smtplib
import ssl

from datetime import date
from email.message import EmailMessage
from typing import Literal

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, EmailStr

from app.repositories.reportes_repo import ReportesRepository

from app.services.reportes_service import (
    generar_pdf_postulaciones,
    generar_excel_postulaciones
)


router = APIRouter(
    prefix="/reportes",
    tags=["Generación de reportes"]
)

repo = ReportesRepository()


# ==========================================
# MODELO PARA ENVÍO DE CORREO
# ==========================================

class EnviarReporteRequest(BaseModel):
    correo_destino: EmailStr
    formato: Literal["pdf", "excel", "ambos"]


# ==========================================
# VALIDACIONES Y CONSULTA
# ==========================================

def validar_fechas(fecha_inicio, fecha_fin):
    if fecha_inicio and fecha_fin and fecha_inicio > fecha_fin:
        raise HTTPException(
            status_code=400,
            detail="La fecha inicial no puede ser posterior a la fecha final."
        )


def obtener_datos_postulaciones(
    fecha_inicio=None,
    fecha_fin=None,
    estado=None,
    empresa=None
):
    validar_fechas(fecha_inicio, fecha_fin)

    try:
        return repo.obtener_reporte_postulaciones(
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            estado=estado,
            empresa=empresa
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Error al obtener el reporte de postulaciones."
        )


# ==========================================
# ENVÍO DE CORREOS CON GMAIL
# ==========================================

def enviar_correo_reporte(destinatario, archivos):

    smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")

    if not smtp_user or not smtp_password:
        raise HTTPException(
            status_code=500,
            detail="La configuración de Gmail no está completa en Render."
        )

    mensaje = EmailMessage()

    mensaje["Subject"] = "Reporte de postulaciones - UniPrácticas"
    mensaje["From"] = smtp_user
    mensaje["To"] = destinatario

    mensaje.set_content(
        """
Hola,

Adjuntamos el reporte de postulaciones generado desde UniPrácticas.

Los archivos solicitados se encuentran adjuntos a este correo.

Saludos,
Sistema UniPrácticas
        """
    )

    for nombre, contenido, tipo in archivos:
        mensaje.add_attachment(
            contenido,
            maintype="application",
            subtype=tipo,
            filename=nombre
        )

    try:
        contexto = ssl.create_default_context()

        with smtplib.SMTP(
            smtp_host,
            smtp_port,
            timeout=30
        ) as servidor:

            servidor.ehlo()
            servidor.starttls(context=contexto)
            servidor.ehlo()

            servidor.login(smtp_user, smtp_password)
            servidor.send_message(mensaje)

    except Exception:
        raise HTTPException(
            status_code=502,
            detail="No fue posible enviar el correo. Verifica la configuración de Gmail."
        )


# ==========================================
# CONSULTAR REPORTE
# ==========================================

@router.get("/postulaciones")
def reporte_postulaciones(
    fecha_inicio: date = Query(None),
    fecha_fin: date = Query(None),
    estado: str = Query(None),
    empresa: str = Query(None)
):

    datos = obtener_datos_postulaciones(
        fecha_inicio,
        fecha_fin,
        estado,
        empresa
    )

    return {
        "total_registros": len(datos),
        "datos": datos
    }


# ==========================================
# DESCARGAR PDF
# ==========================================

@router.get("/postulaciones/pdf")
def descargar_pdf_postulaciones(
    fecha_inicio: date = Query(None),
    fecha_fin: date = Query(None),
    estado: str = Query(None),
    empresa: str = Query(None)
):

    datos = obtener_datos_postulaciones(
        fecha_inicio,
        fecha_fin,
        estado,
        empresa
    )

    try:
        archivo = generar_pdf_postulaciones(datos)

        return StreamingResponse(
            archivo,
            media_type="application/pdf",
            headers={
                "Content-Disposition":
                'attachment; filename="reporte_postulaciones.pdf"'
            }
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Error al generar el PDF."
        )


# ==========================================
# DESCARGAR EXCEL
# ==========================================

@router.get("/postulaciones/excel")
def descargar_excel_postulaciones(
    fecha_inicio: date = Query(None),
    fecha_fin: date = Query(None),
    estado: str = Query(None),
    empresa: str = Query(None)
):

    datos = obtener_datos_postulaciones(
        fecha_inicio,
        fecha_fin,
        estado,
        empresa
    )

    try:
        archivo = generar_excel_postulaciones(datos)

        return StreamingResponse(
            archivo,
            media_type=(
                "application/vnd.openxmlformats-officedocument."
                "spreadsheetml.sheet"
            ),
            headers={
                "Content-Disposition":
                'attachment; filename="reporte_postulaciones.xlsx"'
            }
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Error al generar el Excel."
        )


# ==========================================
# ENVIAR REPORTE POR CORREO
# ==========================================

@router.post("/postulaciones/enviar")
def enviar_reporte_postulaciones(
    solicitud: EnviarReporteRequest,
    fecha_inicio: date = Query(None),
    fecha_fin: date = Query(None),
    estado: str = Query(None),
    empresa: str = Query(None)
):

    datos = obtener_datos_postulaciones(
        fecha_inicio,
        fecha_fin,
        estado,
        empresa
    )

    archivos = []

    try:

        # Generar PDF
        if solicitud.formato in ("pdf", "ambos"):

            pdf = generar_pdf_postulaciones(datos)
            pdf.seek(0)

            archivos.append((
                "reporte_postulaciones.pdf",
                pdf.read(),
                "pdf"
            ))

        # Generar Excel
        if solicitud.formato in ("excel", "ambos"):

            excel = generar_excel_postulaciones(datos)
            excel.seek(0)

            archivos.append((
                "reporte_postulaciones.xlsx",
                excel.read(),
                "vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            ))

        # Enviar archivos por Gmail
        enviar_correo_reporte(
            str(solicitud.correo_destino),
            archivos
        )

        return {
            "mensaje": "Reporte enviado correctamente.",
            "destinatario": str(solicitud.correo_destino),
            "archivos_enviados": [
                archivo[0] for archivo in archivos
            ],
            "total_registros": len(datos)
        }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Ocurrió un error al generar o enviar los reportes."
        )
