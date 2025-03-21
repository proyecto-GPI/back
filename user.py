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

class register_user(BaseModel):
    correo: str
    contraseña: str
    nombre: str
    DNI: str
    tipo: str

router1 = APIRouter()
router2 = APIRouter()



@router1.get("/api/login")
async def enviar_datosH(login_data: user_psw, url: str):
    # Convertir los datos del modelo Pydantic a un diccionario
    login_dict = login_data.dict()

    # Enviar los datos al endpoint especificado
    async with httpx.AsyncClient() as client: #De esta forma, se envian los datos simultaneamente mientras espero una respuesta
        response = await client.post(url, json=login_dict)

    # Devolver la respuesta del servidor(Se decodifica y se devuelve en formato json)
    return json.loads(response.content.decode())



