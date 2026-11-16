
from datetime import date
from typing import Literal

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, EmailStr

from app.repositories.reportes_repo import ReportesRepository

from app.services.reportes_service import (
    generar_pdf_postulaciones,
    generar_excel_postulaciones
)

from app.services.email_service import enviar_email


router = APIRouter(
    prefix="/reportes",
    tags=["Generación de reportes"]
)

repo = ReportesRepository()


# ==========================================
# MODELO PARA SOLICITAR EL ENVÍO DEL REPORTE
# ==========================================

class EnviarReporteRequest(BaseModel):
    correo_destino: EmailStr
    formato: Literal["pdf", "excel", "ambos"]


# ==========================================
# VALIDACIÓN DE FECHAS
# ==========================================

def validar_fechas(fecha_inicio, fecha_fin):

    if fecha_inicio and fecha_fin and fecha_inicio > fecha_fin:
        raise HTTPException(
            status_code=400,
            detail="La fecha inicial no puede ser posterior a la fecha final."
        )


# ==========================================
# OBTENER DATOS DEL REPORTE
# ==========================================

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

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener el reporte: {str(e)}"
        )


# ==========================================
# CONSULTAR REPORTE DE POSTULACIONES
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
# DESCARGAR REPORTE EN PDF
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

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al generar el PDF: {str(e)}"
        )


# ==========================================
# DESCARGAR REPORTE EN EXCEL
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

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al generar el Excel: {str(e)}"
        )


# ==========================================
# ENVIAR REPORTE POR CORREO ELECTRÓNICO
# ==========================================

@router.post("/postulaciones/enviar")
def enviar_reporte_postulaciones(
    solicitud: EnviarReporteRequest,
    fecha_inicio: date = Query(None),
    fecha_fin: date = Query(None),
    estado: str = Query(None),
    empresa: str = Query(None)
):

    # Obtener los datos con los filtros seleccionados
    datos = obtener_datos_postulaciones(
        fecha_inicio,
        fecha_fin,
        estado,
        empresa
    )

    archivos = []

    try:

        # Generar PDF
        if solicitud.formato in ["pdf", "ambos"]:

            pdf = generar_pdf_postulaciones(datos)

            archivos.append((
                "reporte_postulaciones.pdf",
                pdf.getvalue(),
                "pdf"
            ))

        # Generar Excel
        if solicitud.formato in ["excel", "ambos"]:

            excel = generar_excel_postulaciones(datos)

            archivos.append((
                "reporte_postulaciones.xlsx",
                excel.getvalue(),
                "vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            ))

        # Enviar correo con los archivos adjuntos
        enviar_email(
            destinatario=str(solicitud.correo_destino),
            asunto="Reporte de postulaciones - UniPrácticas",
            contenido=(
                "Hola,\n\n"
                "Adjuntamos el reporte de postulaciones solicitado "
                "desde la plataforma UniPrácticas.\n\n"
                f"Total de registros: {len(datos)}\n\n"
                "Saludos,\n"
                "Sistema UniPrácticas"
            ),
            archivos=archivos
        )

        return {
            "mensaje": "Reporte enviado correctamente.",
            "destinatario": str(solicitud.correo_destino),
            "formato": solicitud.formato,
            "total_registros": len(datos)
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Error al enviar el reporte: {str(e)}"
        )
