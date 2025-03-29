from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Oficina  

router5 = APIRouter()

@router5.get("/api/oficinas")
async def get_all_offices(db: Session = Depends(get_db)):
    oficinas = db.query(Oficina).all()  
    return oficinas
