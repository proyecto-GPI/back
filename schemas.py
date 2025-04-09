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