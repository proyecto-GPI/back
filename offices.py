from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Oficina 
from pydantic import BaseModel

router5 = APIRouter()
router10 = APIRouter()
router11 = APIRouter()

class Oficina_create(BaseModel):
    id_oficina: int
    nombre: str
    direccion: str
    ciudad: str

@router5.get("/api/oficinas")
async def get_all_offices(db: Session = Depends(get_db)):
    oficinas = db.query(Oficina).all()  
    return oficinas

@router10.post("/api/add_oficinas")
async def add_offices(oficina: Oficina_create, db: Session = Depends(get_db)):
    #Comprobar oficina existe
    oficina_existente = db.query(Oficina).filter(Oficina.id_oficina == oficina.id_oficina).first()
    if oficina_existente:
        raise HTTPException(status_code=400, detail="Office already exists")
    # Crear una nueva oficina
    nueva_oficina = Oficina(
        id_oficina=oficina.id_oficina,
        nombre=oficina.nombre,
        direccion=oficina.direccion,
        ciudad=oficina.ciudad
    )

    db.add(nueva_oficina)
    db.commit()
    db.refresh(nueva_oficina)
    return db.query(Oficina).all() 

    
@router11.delete("/api/delete_oficinas/{id_oficina}")
async def delete_offices(id_oficina: int, db: Session = Depends(get_db)):
    oficina = db.query(Oficina).filter(Oficina.id_oficina == id_oficina).first()
    
    if oficina:
        db.delete(oficina)
        db.commit()
        return {"detail": "Office deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Office not found")

    
    