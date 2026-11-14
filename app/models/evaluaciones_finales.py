from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class EvaluacionesFinales(BaseModel):
    id_evaluacion: Optional[int] = None
    id_practica: int
    id_evaluador: int
    tipo_evaluacion: str
    fecha_evaluacion: Optional[date] = None
    resultado: Optional[str] = None
    calificacion: Optional[float] = Field(default=None, ge=0)
    cumplimiento_objetivos: Optional[str] = None
    desempeno: Optional[str] = None
    fortalezas: Optional[str] = None
    aspectos_mejora: Optional[str] = None
    observaciones: Optional[str] = None
    recomendaciones: Optional[str] = None
    estado: str