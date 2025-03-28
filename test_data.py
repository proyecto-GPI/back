# test_data.py
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from models import Office, Users, Booking, Base

# Database connection
DATABASE_URL = "postgresql://autoveloz_creator:autovelozGPI@localhost:5432/autoveloz"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# Initialize session
db = SessionLocal()

# Create test Offices
office1 = Office(address="Calle Mayor, 1, Madrid")
office2 = Office(address="Av. Diagonal, 123, Barcelona")

# Create test Users
user1 = Users(id="12345678A", name="Ana Pérez", email="ana@example.com", password="securepassword1", customer_type="individual")
user2 = Users(id="87654321B", name="Empresa XYZ", email="contact@xyz.com", password="securepassword2", customer_type="business")

# Add offices and users to session
db.add_all([office1, office2, user1, user2])
db.commit()

# Refresh to get autogenerated IDs
db.refresh(office1)
db.refresh(office2)

# Create test Bookings
booking1 = Booking(
    user_id=user1.id,
    pickup_id=office1.id,
    return_id=office2.id,
    status="pending",
    credit_card="1234567812345678",
    pickup_date=datetime.now() + timedelta(days=1),
    return_date=datetime.now() + timedelta(days=7),
    price=150.00
)

booking2 = Booking(
    user_id=user2.id,
    pickup_id=office2.id,
    return_id=office1.id,
    status="confirmed",
    credit_card="8765432187654321",
    pickup_date=datetime.now() + timedelta(days=3),
    return_date=datetime.now() + timedelta(days=10),
    price=450.00
)

# Add bookings to session
db.add_all([booking1, booking2])
db.commit()

print("Datos de prueba creados correctamente.")

db.close()
