# routes/booking.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Reserva
from typing import List

router = APIRouter()

@router.get("/api/bookings")
async def get_bookings(db: Session = Depends(get_db)):
    return db.query(Reserva).order_by(Reserva.id.asc()).all()






