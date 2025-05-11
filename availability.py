from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Coche, Oficina,UbicadoEn
from typing import List
from datetime import datetime
from schemas import CocheOut


router6= APIRouter()
router13= APIRouter()

@router6.get("/api/availability", response_model=list[CocheOut])
async def get_cars_availability(
    id_oficina: int,
    fecha_inicio: str,
    fecha_fin: str,
    db: Session = Depends(get_db)
):
    
    print("Avalability recibe: ",  id_oficina, fecha_inicio, fecha_fin)
    fecha_inicio_date = datetime.strptime(fecha_inicio, '%d/%m/%Y %H:%M:%S')
    fecha_fin_date = datetime.strptime(fecha_fin, '%d/%m/%Y %H:%M:%S')
    print("Availability traduce fechas: ",fecha_inicio_date, fecha_fin_date )
    coches = (
        db.query(Coche)
        .join(UbicadoEn, UbicadoEn.id_coche == Coche.id)
        .filter(
            UbicadoEn.id_oficina == id_oficina,
            fecha_fin_date < UbicadoEn.fecha_hasta,
            fecha_inicio_date > UbicadoEn.fecha_desde
        )
        .all()
    )

    print("Coches: ", coches)

    return coches

"""
@router6.get("/api/availability")
async def get_cars_availability(id_oficina:int, fecha_inicio: str, fecha_fin:str, db: Session= Depends(get_db)) ->list:
    fecha_inicio_date= datetime.strptime(fecha_inicio, '%d/%m/%Y %H:%M:%S')
    fecha_fin_date= datetime.strptime(fecha_fin, '%d/%m/%Y %H:%M:%S')
    coches_id = db.query(UbicadoEn.id_coche).filter(UbicadoEn.id_oficina==id_oficina , fecha_fin < UbicadoEn.fecha_hasta, fecha_inicio > UbicadoEn.fecha_desde).all()
     
    print("Coches ID:")

    print(coches_id)

    return dict(coches_id)

"""

@router13.get("/api/coches", response_model=List[CocheOut])
async def get_all_coches(db: Session = Depends(get_db)):
    """
    Devuelve **todos** los coches registrados en la base de datos,
    sin aplicar filtros de disponibilidad ni de oficina.
    """
    return db.query(Coche).all()
