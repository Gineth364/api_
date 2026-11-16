
from fastapi import APIRouter, HTTPException, Query
from datetime import date
from app.repositories.reportes_repo import ReportesRepository

router = APIRouter(
    prefix="/reportes",
    tags=["Generación de reportes"]
)

repo = ReportesRepository()


@router.get("/postulaciones")
def reporte_postulaciones(
    fecha_inicio: date = Query(None),
    fecha_fin: date = Query(None),
    estado: str = Query(None),
    empresa: str = Query(None)
):
    if fecha_inicio and fecha_fin and fecha_inicio > fecha_fin:
        raise HTTPException(
            status_code=400,
            detail="La fecha inicial no puede ser posterior a la fecha final."
        )

    try:
        datos = repo.obtener_reporte_postulaciones(
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            estado=estado,
            empresa=empresa
        )

        return {
            "total_registros": len(datos),
            "datos": datos
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
