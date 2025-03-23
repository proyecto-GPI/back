# models.py

from sqlalchemy import String, Integer, Column, ForeignKey, Enum, TIMESTAMP, DateTime, CheckConstraint, DECIMAL, Text
from database import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship





class Office(Base):
  __tablename__= 'office'
  id = Column(Integer, primary_key=True, nullable=False)
  address = Column(String(50))
  #should we include the schedule?
  #schedule = Column(String(20))
  
class Users (Base):
  __tablename__= 'users'
  # the id will be the DNI of the user
  id=Column(String(9), primary_key=True, nullable=False)
  name = Column(String(20))
  email = Column(String(20))
  password = Column(Text, nullable=False)
  customer_type = Column(Enum('individual', 'business', name="customer_type"), nullable=True)
  # admin s/n?

class Booking (Base):
  __tablename__= 'booking'
  id=Column(Integer, primary_key=True, nullable=False)
  user_id = Column(String(9), ForeignKey('users.id'), nullable=False)
  #n_plate = Column(String(15), ForeignKey('car.n_plate'), nullable=False)
  #budget_id = Column(Integer, ForeignKey(budget.id), nullable=False)
  pickUp_id = Column(Integer, ForeignKey('office.id'), nullable=False)
  return_id = Column(Integer, ForeignKey('office.id'), nullable=False)
  status = Column(Enum('pending', 'confirmed', 'cancelled', 'completed', name="status"), nullable=False)
  credit_card = Column(String(16), nullable = False)
  booking_date = Column(TIMESTAMP(timezone=True), server_default=func.now())
  pickUp_date = Column(DateTime, nullable=False)
  return_date = Column(DateTime, nullable=False)
  price = Column(DECIMAL(10,2))  

  __table_args__ = (
        CheckConstraint("LENGTH(credit_card) = 16 AND credit_card ~ '^[0-9]+$'", name="valid_credit_card")
    )


