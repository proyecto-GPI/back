from pydantic import BaseModel
from typing import Literal

class CocheOut(BaseModel):
    id: int
    techo_solar: bool
    puertas: int
    tipo_cambio: Literal["a", "m"]
    modelo: str
    categoria: Literal["alta", "media", "baja"]

    class Config:
        orm_mode = True

class TarifaOut(BaseModel):
    id_tarifa: int
    tipo_tarifa: Literal["diaria", "diaria_ilimitada", "semanal", "fin_de_semana", "mensual"]
    periodo: Literal["0", "1", "2", "3"]
    precio_por_unidad: float

    class Config:
        orm_mode = True
