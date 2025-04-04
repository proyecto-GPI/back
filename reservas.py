from __future__ import annotations
from fastapi import APIRouter, HTTPException
from fastapi import FastAPI, Query
import httpx
from psycopg2 import IntegrityError
from pydantic import BaseModel, validator
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, Literal 
from sqlalchemy.orm import sessionmaker
import models
import json

from global_variables import id_user

router7 = APIRouter()
router8 = APIRouter()

class Reserve(BaseModel):
    id_oficina: int
    id_coche: int
    fecha_reserva: str
    fecha_recogida: str
    fecha_devolucion: str
    num_tarjeta: str

@router7.post("/api/{id_user}/reserve")
async def reservar(reserve_data: Reserve):
    reserve_dict = reserve_data.dict()
    url= "http://127.0.0.1:8000/api/"+id_user+"rreserve"

    # Enviar los datos al endpoint especificado
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=reserve_dict)

    # Manejar casos donde la respuesta no tiene JSON
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error al mandar la reserva")

    try:
        # Decodificar el contenido JSON
        return json.loads(response.content.decode())
    
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Respuesta inválida del servidor de reserva")


@router8.post("/api/{id_user}/rreserve")
async def rreserve(reserve_data: dict):  # Recibe un diccionario con los datos de la reserva
    session = None
    try:
        # Crear una sesión para la base de datos
        Session = sessionmaker(bind=engine)
        session = Session()
        print("Datos recibidos:", reserve_data)

        # Validar los campos requeridos
        required_fields = ['id_oficina', 'id_coche', 'fecha_reserva', 'fecha_recogida', 'fecha_devolucion', 'num_tarjeta']
        for field in required_fields:
            if field not in reserve_data:
                raise HTTPException(status_code=400, detail=f"El campo {field} es requerido.")

        # Verificar que la oficina y el coche existen
        oficina_recogida = session.query(models.Oficina).filter(models.Oficina.id_oficina == reserve_data['id_oficina']).first()
        coche = session.query(models.Coche).filter(models.Coche.id == reserve_data['id_coche']).first()
        #usuario = session.query(models.Usuario).filter(models.Usuario.id == id_user).first()

        if not oficina_recogida or not coche:
            raise HTTPException(status_code=404, detail="Oficina o coche no encontrado")

        # Crear la reserva
        nueva_reserva = models.Reserva(
            id_oficina_recogida_real=reserve_data['id_oficina'],
            id_coche=reserve_data['id_coche'],
            fecha_reserva=reserve_data['fecha_reserva'],
            fecha_recogida_real=reserve_data['fecha_recogida'],
            fecha_devolucion_real=reserve_data['fecha_devolucion'],
            num_tarjeta=reserve_data['num_tarjeta'],
            estado_reserva="reservado",  # Estado inicial de la reserva
            id_usuario=id_user  # Asociamos la reserva con el usuario
        )

        # Crear el estado de la reserva (relación con Estado_reserva)
        estado_reserva = models.Estado_reserva(
            id_estado="pendiente",  # Estado inicial
            fecha_desde=datetime.now(),  # Fecha desde el momento de la creación de la reserva
            id_reserva=nueva_reserva.id_reserva  # Relacionamos el estado con la reserva
        )

        # Crear la relación entre la reserva y la oficina de devolución
        oficina_devolucion = oficina_recogida  # Para este ejemplo, usamos la misma oficina para recogida y devolución

        # Asignar la reserva al coche
        nueva_reserva.reserva_tiene_coche.append(coche)

        # Añadir la nueva reserva y el estado a la sesión
        session.add(nueva_reserva)
        session.add(estado_reserva)

        # Guardar en la base de datos
        session.commit()
        session.refresh(nueva_reserva)
        session.refresh(estado_reserva)

        # Cerrar la sesión
        session.close()

        return {
            "id_reserva": nueva_reserva.id_reserva,
            "estado_reserva": nueva_reserva.estado_reserva
        }
    
    except IntegrityError as e:
        print(f"Error al procesar la reserva: {e}")
        session.rollback()
        raise HTTPException(status_code=500, detail="Error interno al procesar la reserva")
    
    finally:
        if session:
            session.close()
    