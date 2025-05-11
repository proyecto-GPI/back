from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session
from database import get_db
from models import Tarifa, Modelo, modelo_tarifa
from schemas import TarifaOut
from typing import List

router12= APIRouter()
router14= APIRouter()

# Función auxiliar para calcular el periodo
def obtener_periodo(fecha_inicio: datetime, fecha_fin: datetime):
    if fecha_inicio.month >= 1 and fecha_inicio.month <= 5:
        return "1"
    elif fecha_inicio.month >= 6 and fecha_inicio.month <= 9:
        return "2"
    elif fecha_inicio.month >= 10 and fecha_inicio.month <= 12:
        return "3"
    return None

@router12.get("/api/tarifas")
#necesito: modelo, gama, fecha inicio, fecha fin [para saber temporada]
#devuelvo: id_tarifa, tipo_tarifa, periodo, precio_base, precio aplicando los dias alquilados
async def get_tarifas(
    modelo: str,
    gama: str,
    fecha_inicio: str,
    fecha_fin: str,
    db: Session = Depends(get_db)
):
    
    try:
        fecha_inicio_dt = datetime.strptime(fecha_inicio, "%Y-%m-%d")
        fecha_fin_dt = datetime.strptime(fecha_fin, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de fecha inválido. Usa YYYY-MM-DD")

    try:
        periodo = obtener_periodo(fecha_inicio_dt, fecha_fin_dt)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Error en las fechas: {str(e)}")
    except Exception:
        raise HTTPException(status_code=500, detail="Error al calcular el periodo de temporada.")


    tarifas = db.query(Tarifa).join(modelo_tarifa).join(Modelo).filter(
        Modelo.modelo == modelo,
        Modelo.categoria == gama,
        or_(
            and_(
                Tarifa.tipo_tarifa == "diaria_ilimitada",
                Tarifa.periodo == periodo
            ),
            and_(
                Tarifa.tipo_tarifa == "mensual",
                Tarifa.periodo == "0"
            )
        )
    ).order_by(
    Tarifa.tipo_tarifa == "diaria_ilimitada", 
    Tarifa.tipo_tarifa == "mensual"
    ).all()

    if not tarifas:
        raise HTTPException(status_code=404, detail="No se encontraron tarifas para esos criterios")

    #calcular el precio final 
    # días totales
    dias_alquiler = (fecha_fin_dt - fecha_inicio_dt).days

    # Supone 1 mes = 30 días
    meses_alquiler = dias_alquiler // 30
    if dias_alquiler % 30 !=0:
        meses_alquiler += 1
    
    unidades = [dias_alquiler, meses_alquiler]

    return [
        {
            "id_tarifa": tarifa.id_tarifa,
            "tipo_tarifa": tarifa.tipo_tarifa,
            "periodo": tarifa.periodo,
            "precio_por_unidad": tarifa.precio_por_unidad,
            "precio_total": tarifa.precio_por_unidad*unidades[u]
        }
        for tarifa, u in tarifas
    ]

@router14.get("/api/tarifas/all", response_model=List[TarifaOut])
async def get_all_tarifas(db: Session = Depends(get_db)):
    """
    Devuelve **todas** las tarifas registradas, sin aplicar filtros
    de modelo, gama ni temporada.
    """
    return db.query(Tarifa).all()
