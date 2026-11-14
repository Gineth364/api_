from pydantic import BaseModel, Field, model_validator
from typing import Optional
from datetime import date


class Puestos_practica(BaseModel):
    id_puesto: Optional[int] = None
    id_empresa: int
    titulo: str
    descripcion: str
    requisitos: str
    area: str
    modalidad: str
    fecha_inicio: date
    fecha_fin: date
    estado: str
    cupos_disponibles: int = Field(ge=0)

    @model_validator(mode="after")
    def validar_fechas(self):
        if self.fecha_fin < self.fecha_inicio:
            raise ValueError("fecha_fin no puede ser anterior a fecha_inicio")
        return self
