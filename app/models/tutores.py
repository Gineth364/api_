
from pydantic import BaseModel
from typing import Optional


class Usuario(BaseModel):
    id_tutor: Optional[int] = None
    especialidad: str
    cargo: str
    estado: bool
