from __future__ import annotations
from fastapi import APIRouter
from fastapi import FastAPI, Query
import httpx
from pydantic import BaseModel, validator
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, Literal 

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
    print("Sesión iniciada correctamente")
    user_id = {"usr_id": "12345"}  # Devuelve un diccionario válido
    return user_id


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

@router4.post("/api/registerok")
async def rlogin(register_data: register_user):  # Recibe un diccionario con los datos del usuario
    print("Registro completado correctamente")
    ok = True
    return ok

