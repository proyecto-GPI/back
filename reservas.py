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
from database import engine


router7 = APIRouter()
router8 = APIRouter()

class Reserve(BaseModel):
    id_user: str #Lo proporciona front
    id_oficina: int
    id_coche: int
    fecha_recogida: str
    fecha_devolucion: str
    num_tarjeta: str


@router7.post("/api/reserve")
async def reservar(reserve_data: Reserve):
    reserve_dict = reserve_data.dict()
    url= "http://127.0.0.1:8000/api/rreserve"

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


@router8.post("/api/rreserve")
async def rreserve(reserve_data: dict):  # Recibe un diccionario con los datos de la reserva
    session = None
    try:
        # Crear una sesión para la base de datos
        Session = sessionmaker(bind=engine)
        session = Session()
        print("Datos recibidos:", reserve_data)

        required_fields = ['id_oficina', 'id_coche', 'fecha_recogida', 'fecha_devolucion', 'num_tarjeta', 'id_user']
        for field in required_fields:
            if not reserve_data.get(field):
                raise HTTPException(status_code=400, detail=f"El campo {field} es requerido.")


        # Verificar que la oficina y el coche existen
        oficina_recogida = session.query(models.Oficina).filter(models.Oficina.id_oficina == reserve_data['id_oficina']).first()
        coche = session.query(models.Coche).filter(models.Coche.id == reserve_data['id_coche']).first()
        #usuario = session.query(models.Usuario).filter(models.Usuario.id == id_user).first()

        if not oficina_recogida or not coche:
            raise HTTPException(status_code=404, detail="Oficina o coche no encontrado")


        # Crear la nueva reserva
        nueva_reserva = models.Reserva(
            oficina_recogida_propuesta=reserve_data['id_oficina'],
            oficina_devolucion_propuesta=reserve_data['id_oficina'],  # Usa la misma oficina por defecto
            fecha_recogida_propuesta=datetime.strptime(reserve_data['fecha_recogida'], "%Y-%m-%d").date(),
            fecha_devolucion_propuesta=datetime.strptime(reserve_data['fecha_devolucion'], "%Y-%m-%d").date(),
            fecha_confirmacion=datetime.now().date(),  # Fecha actual en formato YYYY-MM-DD
            importe_final_previsto=100.0,  # Valor por defecto, puedes calcular según lógica
            num_tarjeta=reserve_data['num_tarjeta'],  # Validado previamente como numérico
            fecha_recogida_real=datetime.strptime(reserve_data['fecha_recogida'], "%Y-%m-%d").date(),
            fecha_devolucion_real=datetime.strptime(reserve_data['fecha_devolucion'], "%Y-%m-%d").date(),
            id_usuario=reserve_data['id_user'],
            id_coche=reserve_data['id_coche'],
            id_oficina_recogida_real=reserve_data['id_oficina'],
            id_oficina_devolucion_real=reserve_data['id_oficina']
        )

        # Añadir la nueva reserva a la sesión y guardar en la base de datos
        session.add(nueva_reserva)
        session.commit()
        session.refresh(nueva_reserva)

        # Crear el estado inicial de la reserva
        estado_reserva = models.Estado_reserva(
            id_estado="pendiente",
            fecha_desde=datetime.now(),  # Fecha actual para el estado
            id_reserva=nueva_reserva.id_reserva
        )
        

        nueva_reserva.reserva_tiene_estado.append(estado_reserva)
        session.add(estado_reserva)
        session.commit()



        # Retornar la información de la reserva y el estado asociado
        return {
            "id_reserva": nueva_reserva.id_reserva,
            "estado_reserva": [estado.id_estado for estado in nueva_reserva.reserva_tiene_estado]
        }


        

    except IntegrityError as e:
        print(f"Error al procesar la reserva: {e}")
        session.rollback()
        raise HTTPException(status_code=500, detail="Error interno al procesar la reserva")
    
    finally:
        if session:
            session.close()
    