# routes/booking.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Booking
from typing import List

router = APIRouter()

@router.get("/api/bookings")
def get_bookings(db: Session = Depends(get_db)):
    return db.query(Booking).order_by(Booking.id.asc()).all()






