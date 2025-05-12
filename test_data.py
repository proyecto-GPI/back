# test_data.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta, date, datetime
from models import Oficina, Usuario, Reserva, Tarifa, modelo_tarifa, Modelo, Coche, UbicadoEn, Base, Tarifa
from sqlalchemy import delete
from decimal import Decimal
from sqlalchemy.exc import IntegrityError

#MIRAR LINEA 173

# Configuración de la base de datos
DATABASE_URL = "postgresql://autoveloz_creator:autovelozGPI@localhost:5432/autoveloz"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# Crear tablas (solo si no existen)
Base.metadata.create_all(bind=engine)

# Iniciar sesión
db = SessionLocal()

# Elimina todas las filas de la tabla
stmt = delete(UbicadoEn)
db.execute(stmt)
db.commit()

stmt = delete(Reserva)
db.execute(stmt)
db.commit()

stmt = delete(Coche)
db.execute(stmt)
db.commit()

stmt = delete(Usuario)
db.execute(stmt)
db.commit()

stmt = delete(modelo_tarifa)
db.execute(stmt)
db.commit()

stmt = delete(Tarifa)
db.execute(stmt)
db.commit()

stmt = delete(Modelo)
db.execute(stmt)
db.commit()

stmt = delete(Oficina)
db.execute(stmt)
db.commit()


# Crear oficinas de prueba
office1 = Oficina(id_oficina = 1, direccion="Calle Mayor, 1, Madrid", nombre="Oficina Madrid", ciudad="Madrid")
office2 = Oficina(id_oficina = 2, direccion="Av. Diagonal, 123, Barcelona",nombre="Oficina Barcelona", ciudad="Barcelona")
office3 = Oficina(id_oficina = 3, direccion="Calle Cañailla, 35, Rota", nombre="Oficina Rota", ciudad="Cádiz")
office4 = Oficina(id_oficina = 4, direccion = "Calle Mártires, 15, Galicia", nombre="Oficina Santiago", ciudad="Santiago")

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

user3 = Usuario(
  id= "ADMIN1234",
  nombre="El Admin",
  correo="admin@admin.com",
  contrasenya="securepassword3",
  tipo_cliente="admin",
  fecha_registro=date.today()
)

# Agregar a la base de datos
db.add_all([office1, office2, office3, office4,  user1, user2, user3])
db.commit()

# Refrescar para obtener IDs generados
db.refresh(office1)
db.refresh(office2)
db.refresh(user1)
db.refresh(user2)
db.refresh(user3)


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


reserva_prueba1 = Reserva(
   
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

reserva_prueba2 = Reserva(
   
    oficina_recogida_propuesta=3,
    oficina_devolucion_propuesta=4,
    fecha_recogida_propuesta=date(2024, 5, 3),
    fecha_devolucion_propuesta=date(2024, 5, 15),
    fecha_confirmacion=date(2024, 5, 1),
    importe_final_previsto=Decimal("350.00"),
    num_tarjeta="8765432112345678",
    fecha_recogida_real=None,
    fecha_devolucion_real=None,
    id_usuario="12345678A",
    id_coche=1,
    id_oficina_recogida_real=None,
    id_oficina_devolucion_real=None,
    id_reserva_padre=None
)
try:
    db.add(reserva_prueba1)
    db.add(reserva_prueba2)
    db.commit()
except IntegrityError:
        db.rollback()
        print(f"Reserva con ID {c.id} ya existe, se omite.")

print("Reserva de prueba creada con éxito.")


ubicadoPrueba1 = UbicadoEn(

     fecha_hasta = date(2025, 5, 3),
     fecha_desde = date(2000, 5, 3),
     id_coche = 1,
     id_oficina = 1
)

ubicadoPrueba2 = UbicadoEn(
     

     fecha_hasta = datetime(2025, 5, 3),
     fecha_desde = datetime(2000, 5, 3),
     id_coche = 2,
     id_oficina = 1
)


try:
    db.add(ubicadoPrueba1)
    db.add(ubicadoPrueba2)
    db.commit()
except IntegrityError:
        db.rollback()
        print(f"UbicadoEn con ID {c.id} ya existe, se omite.")



#---- crear tarifas ----
tarifas = [
    Tarifa(
        tipo_tarifa="diaria_ilimitada", 
        periodo="1", 
        precio_por_unidad=500.0
    ),
    Tarifa(
        tipo_tarifa="mensual", 
        periodo="0", 
        precio_por_unidad=1500.0,  
    ),
    Tarifa(
        tipo_tarifa="diaria_ilimitada", 
        periodo="2", 
        precio_por_unidad=700.0
    ),
     Tarifa(
        tipo_tarifa="mensual", 
        periodo="0", 
        precio_por_unidad=1200.0
    )
]

modelos[0].modelo_tiene_tarifa = [tarifas[0], tarifas[1]]  # Golf GTI 
modelos[1].modelo_tiene_tarifa = [tarifas[1], tarifas[2]]  # Model 3 
modelos[2].modelo_tiene_tarifa = [tarifas[2], tarifas[3]]  # Ibiza FR

# Agregar a la base de datos
for tarifa in tarifas:
    try:
        db.add(tarifa)
        db.commit()
        print(f"Tarifa '{tarifa.tipo_tarifa}' creada para los modelos {', '.join([m.modelo for m in tarifa.tarifa_tiene_modelo])}.")
    except IntegrityError:
        db.rollback()
        print(f"Tarifa '{tarifa.tipo_tarifa}' ya existe o hubo un error al agregarla.")



print("✅ Datos de prueba creados correctamente.")

db.close()
