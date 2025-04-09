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
from datetime import datetime, timedelta, date, datetime

import models
from database import engine
import json


router1 = APIRouter()
router2 = APIRouter()
router3 = APIRouter()
router4 = APIRouter()

# Aquí defines tus endpoints
class UserLogin(BaseModel):
    correo: str
    contrasenya: str

class UserID(BaseModel):
    id_user: str = None

# Variable global para mantener el estado
global_user_id_instance = UserID()

class UserRegister(BaseModel):
    id: str
    correo: str
    nombre: str
    contrasenya: str
    tipo_cliente: Literal['negocio', 'particular', 'admin']
  

class register_state(BaseModel):
    ok: bool



@router1.post("/api/login")
async def login(login_data: UserLogin):
    # Convertir los datos del modelo Pydantic a un diccionario
    login_dict = login_data.dict()
    url = "http://127.0.0.1:8000/api/rlogin"

    # Enviar los datos al endpoint especificado
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=login_dict)

    # Manejar casos donde la respuesta no tiene JSON
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error en la autenticación")

    try:
        # Decodificar el contenido JSON
        response_data = json.loads(response.content.decode())
        id_user = response_data.get('id')
        print("ID actualizado:", id_user)
        global_user_id_instance.id_user = id_user
        return response_data
    
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Respuesta inválida del servidor de autenticación")



@router2.post("/api/rlogin")
async def rlogin(usuario_data: dict):  # Recibe un diccionario con los datos del usuario
    session = None
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        print("Datos recibidos:", usuario_data)
        
        # Validar que el diccionario tenga los campos necesarios
        required_fields = ['correo', 'contrasenya']
        for field in required_fields:
            if field not in usuario_data:
                raise HTTPException(status_code=400, detail=f"El campo {field} es requerido.")
 
        # Buscar al usuario en la base de datos
        usuario_db = session.query(models.Usuario).filter(models.Usuario.correo == usuario_data['correo']).first()

        if not usuario_db:
            raise HTTPException(status_code=404, detail="El email del usuario es incorrecto.")
        
        # Validar la contraseña directamente como texto plano (solo para pruebas)
        if usuario_data['contrasenya'] != usuario_db.contrasenya:
            raise HTTPException(status_code=404, detail="Contraseña incorrecta.")
 
        print(f"Sesión iniciada correctamente id : {usuario_db.id}")
        return {"detail": "Sesión iniciada correctamente", "id": usuario_db.id}
    except Exception as e:
        print("Error inesperado:", e)
        raise HTTPException(status_code=500, detail="Error interno al iniciar sesión")
    finally:
        if session:
            session.close()



@router3.post("/api/register")
async def register(register_data: UserRegister):
    register_dict = register_data.dict()
    url = "http://127.0.0.1:8000/api/okregister"

    # Enviar los datos al endpoint especificado
    async with httpx.AsyncClient() as client: #De esta forma, se envian los datos simultaneamente mientras espero una respuesta
        response = await client.post(url, json=register_dict)

    if (response.json()):
        return "Registro completado"
    else: 
        return "Registro inválido"

@router4.post("/api/okregister")
async def okregister(register_data: UserRegister):  # Recibe un diccionario con los datos del usuario
    session = None
    try:
        # Agregar usuario a la base de datos
        Session = sessionmaker(bind=engine)
        session = Session()
        nuevo_usuario = models.Usuario(
            id=register_data.id,
            nombre=register_data.nombre,
            correo=register_data.correo,
            contrasenya=register_data.contrasenya,  # ⚠️ Para pruebas, en texto plano
            tipo_cliente=register_data.tipo_cliente,
            fecha_registro=date.today()  # ⬅️ Añade esto si es requerido y no viene en register_data
        )

        session.add(nuevo_usuario)
        session.commit()

        print("Registro completado correctamente")
        return {"detail": "Usuario registrado exitosamente"}  # Responde con código 200 por defecto
    except Exception as e:
        print("Error en el registro:", e)
        raise HTTPException(status_code=500, detail="Error interno al registrar usuario")
    finally:
        if session:
            session.close()
