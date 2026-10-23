from pydantic import BaseModel
from typing import Optional


class Usuario(BaseModel):
    id_estudiante: Optional[int] = None
    codigo_estudiantil: str
    programa_academico: str
    semestre: int
    estado_academico: bool