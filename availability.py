from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Coche, Oficina,UbicadoEn
from typing import List
from datetime import datetime


router6= APIRouter()

@router6.get("/api/availability")
async def get_cars_availability(id_oficina:int, fecha_inicio: str, fecha_fin:str, db: Session= Depends(get_db)) ->list:
    fecha_inicio_date= datetime.strptime(fecha_inicio, '%d/%m/%Y %H:%M:%S')
    fecha_fin_date= datetime.strptime(fecha_fin, '%d/%m/%Y %H:%M:%S')
    coches_id:list = db.query(UbicadoEn.id_coche).filter(UbicadoEn.id_oficina==id_oficina , fecha_fin < UbicadoEn.fecha_hasta, fecha_inicio > UbicadoEn.fecha_desde).all()
    return coches_id