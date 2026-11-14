from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Postulaciones(BaseModel):
    id_postulacion: Optional[int] = None
    id_estudiante: int
    id_puesto: int
    fecha_postulacion: datetime
    estado: str
    comentarios: Optional[str] = None