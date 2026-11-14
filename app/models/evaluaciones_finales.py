from pydantic import BaseModel
from typing import Optional
from datetime import date


class EvaluacionesFinales(BaseModel):
    id_evaluacion: Optional[int] = None
    id_practica: int
    id_evaluador: Optional[int] = None
    tipo_evaluacion: str
    fecha_evaluacion: Optional[date] = None
    resultado: Optional[str] = None
    calificacion: Optional[float] = None
    cumplimiento_objetivos: Optional[str] = None
    desempeno: Optional[str] = None
    fortalezas: Optional[str] = None
    aspectos_mejora: Optional[str] = None
    observaciones: Optional[str] = None
    recomendaciones: Optional[str] = None
    estado: str