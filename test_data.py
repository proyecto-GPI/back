# test_data.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta, date
from models import Oficina, Usuario, Reserva, Modelo, Coche, Base
from sqlalchemy import delete
from decimal import Decimal
from sqlalchemy.exc import IntegrityError


# Configuración de la base de datos
DATABASE_URL = "postgresql://autoveloz_creator:autovelozGPI@localhost:5432/autoveloz"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# Crear tablas (solo si no existen)
Base.metadata.create_all(bind=engine)

# Iniciar sesión
db = SessionLocal()

# Elimina todas las filas de la tabla
stmt = delete(Oficina)
db.execute(stmt)
db.commit()

stmt = delete(Usuario)
db.execute(stmt)
db.commit()

stmt = delete(Coche)
db.execute(stmt)
db.commit()

stmt = delete(Modelo)
db.execute(stmt)
db.commit()

# Crear oficinas de prueba
office1 = Oficina(id_oficina = 1, direccion="Calle Mayor, 1, Madrid")
office2 = Oficina(id_oficina = 2, direccion="Av. Diagonal, 123, Barcelona")
office3 = Oficina(id_oficina = 3, direccion="Calle Cañailla, 35, Rota")
office4 = Oficina(id_oficina = 4, direccion = "Calle Mártires, 15, Galicia")

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
db.add_all([office1, office2, office3, office4,  user1, user2])
db.commit()

# Refrescar para obtener IDs generados
db.refresh(office1)
db.refresh(office2)
db.refresh(user1)
db.refresh(user2)


modelos = [
    Modelo(modelo="Golf GTI", marca="Volkswagen", categoria="media"),
    Modelo(modelo="Model 3", marca="Tesla", categoria="alta"),
    Modelo(modelo="Ibiza FR", marca="SEAT", categoria="baja")
]

for m in modelos:
    try:
        db.add(m)
        db.commit()
        print(f"Modelo '{m.modelo}' creado.")
    except IntegrityError:
        db.rollback()
        print(f"Modelo '{m.modelo}' ya existe, se omite.")

# ----- Crear coches -----
coches = [
    Coche(id=1, modelo="Golf GTI", categoria="media", tipo_cambio='m', techo_solar=True, puertas=5),
    Coche(id=2, modelo="Model 3", categoria="alta", tipo_cambio='a', techo_solar=True, puertas=4),
    Coche(id=3, modelo="Ibiza FR", categoria="baja", tipo_cambio='m', techo_solar=False, puertas=3),
    Coche(id=4, modelo="Golf GTI", categoria="media", tipo_cambio='a', techo_solar=False, puertas=5)
]

for c in coches:
    try:
        db.add(c)
        db.commit()
        print(f"Coche con ID {c.id} creado.")
    except IntegrityError:
        db.rollback()
        print(f"Coche con ID {c.id} ya existe, se omite.")


reserva_prueba = Reserva(
    id_reserva=1,
    oficina_recogida_propuesta=1,
    oficina_devolucion_propuesta=2,
    fecha_recogida_propuesta=date(2024, 4, 10),
    fecha_devolucion_propuesta=date(2024, 4, 15),
    fecha_confirmacion=date(2024, 4, 1),
    importe_final_previsto=Decimal("250.00"),
    num_tarjeta="1234567812345678",
    fecha_recogida_real=None,
    fecha_devolucion_real=None,
    id_usuario="12345678A",
    id_coche=1,
    id_oficina_recogida_real=None,
    id_oficina_devolucion_real=None,
    id_reserva_padre=None
)
try:
    db.add(reserva_prueba)
    db.commit()
except IntegrityError:
        db.rollback()
        print(f"Reserva con ID {c.id} ya existe, se omite.")

print("Reserva de prueba creada con éxito.")

print("✅ Datos de prueba creados correctamente.")

db.close()
