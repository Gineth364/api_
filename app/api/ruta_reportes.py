
from datetime import date

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse

from app.repositories.reportes_repo import ReportesRepository

from app.services.reportes_service import (
    generar_pdf_postulaciones,
    generar_excel_postulaciones,
    generar_pdf_practicas,
    generar_excel_practicas,
    generar_pdf_evaluaciones,
    generar_excel_evaluaciones
)


router = APIRouter(
    prefix="/reportes",
    tags=["Generación de reportes"]
)

repo = ReportesRepository()


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
# OBTENER DATOS DE LOS REPORTES
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
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener el reporte de postulaciones: {str(e)}"
        )


def obtener_datos_practicas(
    fecha_inicio=None,
    fecha_fin=None,
    estado=None,
    empresa=None,
    tutor=None
):
    validar_fechas(fecha_inicio, fecha_fin)

    try:
        return repo.obtener_reporte_practicas(
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            estado=estado,
            empresa=empresa,
            tutor=tutor
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener el reporte de prácticas: {str(e)}"
        )


def obtener_datos_evaluaciones(
    fecha_inicio=None,
    fecha_fin=None,
    estado=None,
    empresa=None,
    tipo_evaluacion=None
):
    validar_fechas(fecha_inicio, fecha_fin)

    try:
        return repo.obtener_reporte_evaluaciones(
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            estado=estado,
            empresa=empresa,
            tipo_evaluacion=tipo_evaluacion
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener el reporte de evaluaciones: {str(e)}"
        )


# ==========================================
# REPORTE DE POSTULACIONES
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
            detail=f"Error al generar el PDF de postulaciones: {str(e)}"
        )


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
            detail=f"Error al generar el Excel de postulaciones: {str(e)}"
        )


# ==========================================
# REPORTE DE PRÁCTICAS
# ==========================================

@router.get("/practicas")
def reporte_practicas(
    fecha_inicio: date = Query(None),
    fecha_fin: date = Query(None),
    estado: str = Query(None),
    empresa: str = Query(None),
    tutor: str = Query(None)
):
    datos = obtener_datos_practicas(
        fecha_inicio,
        fecha_fin,
        estado,
        empresa,
        tutor
    )

    return {
        "total_registros": len(datos),
        "datos": datos
    }


@router.get("/practicas/pdf")
def descargar_pdf_practicas(
    fecha_inicio: date = Query(None),
    fecha_fin: date = Query(None),
    estado: str = Query(None),
    empresa: str = Query(None),
    tutor: str = Query(None)
):
    datos = obtener_datos_practicas(
        fecha_inicio,
        fecha_fin,
        estado,
        empresa,
        tutor
    )

    try:
        archivo = generar_pdf_practicas(datos)

        return StreamingResponse(
            archivo,
            media_type="application/pdf",
            headers={
                "Content-Disposition":
                'attachment; filename="reporte_practicas.pdf"'
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al generar el PDF de prácticas: {str(e)}"
        )


@router.get("/practicas/excel")
def descargar_excel_practicas(
    fecha_inicio: date = Query(None),
    fecha_fin: date = Query(None),
    estado: str = Query(None),
    empresa: str = Query(None),
    tutor: str = Query(None)
):
    datos = obtener_datos_practicas(
        fecha_inicio,
        fecha_fin,
        estado,
        empresa,
        tutor
    )

    try:
        archivo = generar_excel_practicas(datos)

        return StreamingResponse(
            archivo,
            media_type=(
                "application/vnd.openxmlformats-officedocument."
                "spreadsheetml.sheet"
            ),
            headers={
                "Content-Disposition":
                'attachment; filename="reporte_practicas.xlsx"'
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al generar el Excel de prácticas: {str(e)}"
        )


# ==========================================
# REPORTE DE EVALUACIONES
# ==========================================

@router.get("/evaluaciones")
def reporte_evaluaciones(
    fecha_inicio: date = Query(None),
    fecha_fin: date = Query(None),
    estado: str = Query(None),
    empresa: str = Query(None),
    tipo_evaluacion: str = Query(None)
):
    datos = obtener_datos_evaluaciones(
        fecha_inicio,
        fecha_fin,
        estado,
        empresa,
        tipo_evaluacion
    )

    return {
        "total_registros": len(datos),
        "datos": datos
    }


@router.get("/evaluaciones/pdf")
def descargar_pdf_evaluaciones(
    fecha_inicio: date = Query(None),
    fecha_fin: date = Query(None),
    estado: str = Query(None),
    empresa: str = Query(None),
    tipo_evaluacion: str = Query(None)
):
    datos = obtener_datos_evaluaciones(
        fecha_inicio,
        fecha_fin,
        estado,
        empresa,
        tipo_evaluacion
    )

    try:
        archivo = generar_pdf_evaluaciones(datos)

        return StreamingResponse(
            archivo,
            media_type="application/pdf",
            headers={
                "Content-Disposition":
                'attachment; filename="reporte_evaluaciones.pdf"'
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al generar el PDF de evaluaciones: {str(e)}"
        )


@router.get("/evaluaciones/excel")
def descargar_excel_evaluaciones(
    fecha_inicio: date = Query(None),
    fecha_fin: date = Query(None),
    estado: str = Query(None),
    empresa: str = Query(None),
    tipo_evaluacion: str = Query(None)
):
    datos = obtener_datos_evaluaciones(
        fecha_inicio,
        fecha_fin,
        estado,
        empresa,
        tipo_evaluacion
    )

    try:
        archivo = generar_excel_evaluaciones(datos)

        return StreamingResponse(
            archivo,
            media_type=(
                "application/vnd.openxmlformats-officedocument."
                "spreadsheetml.sheet"
            ),
            headers={
                "Content-Disposition":
                'attachment; filename="reporte_evaluaciones.xlsx"'
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al generar el Excel de evaluaciones: {str(e)}"
        )
