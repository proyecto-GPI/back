# test_data.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta, date
from models import Oficina, Usuario, Reserva, Base

# Configuración de la base de datos
DATABASE_URL = "postgresql://autoveloz_creator:autovelozGPI@localhost:5432/autoveloz"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# Crear tablas (solo si no existen)
Base.metadata.create_all(bind=engine)

# Iniciar sesión
db = SessionLocal()

# Crear oficinas de prueba
office1 = Oficina(direccion="Calle Mayor, 1, Madrid")
office2 = Oficina(direccion="Av. Diagonal, 123, Barcelona")

# Crear usuarios de prueba
user1 = Usuario(
    id="12345678A",
    nombre="Ana Pérez",
    correo="ana@example.com",
    contrasenya="securepassword1",
    tipo_cliente="particular",
    fecha_registro=date.today()
)

user2 = Usuario(
    id="87654321B",
    nombre="Empresa XYZ",
    correo="contact@xyz.com",
    contrasenya="securepassword2",
    tipo_cliente="negocio",
    fecha_registro=date.today()
)

# Agregar a la base de datos
db.add_all([office1, office2, user1, user2])
db.commit()

# Refrescar para obtener IDs generados
db.refresh(office1)
db.refresh(office2)
db.refresh(user1)
db.refresh(user2)




print("✅ Datos de prueba creados correctamente.")

db.close()
