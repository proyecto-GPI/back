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
import bscript
import models

import json



class user_psw(BaseModel): 
    correo: str
    contraseña: str
    
class user_id(BaseModel): 
    usr_id: str

class register_user(BaseModel):
    correo: str
    contraseña: str
    nombre: str
    DNI: str
    tipo: str

class register_state(BaseModel):
    ok: bool

router1 = APIRouter()
router2 = APIRouter()
router3 = APIRouter()
router4 = APIRouter()


@router1.post("/api/login")
async def login(login_data: user_psw):
    # Convertir los datos del modelo Pydantic a un diccionario
    login_dict = login_data.dict()
    url = "http://127.0.0.1:8000/api/rlogin"

    # Enviar los datos al endpoint especificado
    async with httpx.AsyncClient() as client: #De esta forma, se envian los datos simultaneamente mientras espero una respuesta
        response = await client.post(url, json=login_dict)
    # Devolver la respuesta del servidor(Se decodifica y se devuelve en formato json)
    return response.json()

@router2.post("/api/rlogin")
async def rlogin(usuario_data: user_psw):  # Recibe un diccionario con los datos del usuario
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
       
        # Validar que el diccionario tenga los campos necesarios
        required_fields = ['email', 'password']
        for field in required_fields:
            if field not in usuario_data:
                raise HTTPException(status_code=400, detail=f"El campo {field} es requerido.")
 
        # Buscar al usuario en la base de datos
        usuario_db = session.query(models.Users).filter(models.Users.email == usuario_data['email']).first()
        if not usuario_db:
            raise HTTPException(status_code=404, detail="El nombre de usuario es incorrecto.")
        if usuario_db.deshabilitado==1:
            raise HTTPException(status_code=403, detail="No se puede loggear un usuario deshabilitado")
       
        # Validar la contraseña
        if not bcrypt.checkpw(usuario_data['password'].encode('utf-8'), usuario_db.password):  # Esto debe ser sustituido por la lógica adecuada
            raise HTTPException(status_code=404, detail="Contraseña incorrecta.")
 
        print("Sesión iniciada correctamente")
        return usuario_db
    except IntegrityError as e:
        print("Error al iniciar sesión:", e)
        raise HTTPException(status_code=500, detail="Error interno al iniciar sesión")
    finally:
        session.close()


@router3.post("/api/register")
async def register(register_data: register_user):
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
async def rlogin(register_data: register_user):  # Recibe un diccionario con los datos del usuario
    print("Registro completado correctamente")
    ok = False
    return ok

