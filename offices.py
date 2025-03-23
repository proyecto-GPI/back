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
import bcrypt
import models

import json

class id_office(BaseModel): 
    id_office: str

class adress(BaseModel):
    adress: str

router5 = APIRouter()

@router5.get("/api/oficinas")
async def get_all_offices():
    url = "http://localhost:8000/api/oficinas"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error al obtener las oficinas")

    return response.json() 
