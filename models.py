# models.py

from sqlalchemy import String, Integer, Column, ForeignKey, Enum, TIMESTAMP, DateTime, CheckConstraint, DECIMAL, Text, Boolean, Table, Double
from database import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship





class Oficina(Base):
  __tablename__= 'oficina'
  id_oficina = Column(Integer, primary_key=True, nullable=False)
  direccion = Column(String(50))
  #should we include the schedule?
  #schedule = Column(String(20))

  ubicado_en = Column(Integer, ForeignKey("coche.id_coche"), nullable=False)

  ubicaciones = relationship("UbicadoEn", back_populates="oficina")

class UbicadoEn(Base):
  __tablename__ = 'ubicado_en'

  fecha_hasta = Column(DateTime, primary_key=True, nullable=False)
  fecha_desde = Column(DateTime)
  
  coche_id = Column(Integer, ForeignKey("coche.id_coche"), nullable=False)  
  oficina_id = Column(Integer, ForeignKey("oficina.id_oficina"), nullable=False) 
  
  # Relación inversa -> REVISAR SI ES CORRECTO
  coche_ubi = relationship("Coche", back_populates="ubicaciones")
  oficina = relationship("Oficina", back_populates="ubicaciones")
  
class Usuario (Base):
  __tablename__= 'usuario'
  # the id will be the DNI of the user
  DNI_usuario=Column(String(9), primary_key=True, nullable=False)
  nombre = Column(String(20))
  correo = Column(String(20))
  contrasenia = Column(Text, nullable=False)
  tipo_cliente = Column(Enum('individual', 'business', name="customer_type"), nullable=True)
  # esperar a ver que enumerados se ponen en el paso a tablas?

  usuario_realiza_reserva =relationship("Reserva", back_populates="reserva_realiza_usuario")

#de momento no hago reserva-----------------------------------------
class Reserva (Base):
  __tablename__= 'reserva'
  n_reserva=Column(Integer, primary_key=True, nullable=False)
  DNI_usuario = Column(String(9), ForeignKey('usuario.DNI_usuario'), nullable=False)
  #n_plate = Column(String(15), ForeignKey('car.n_plate'), nullable=False)
  #budget_id = Column(Integer, ForeignKey(budget.id), nullable=False)
  pickUp_id = Column(Integer, ForeignKey('office.id'), nullable=False)
  return_id = Column(Integer, ForeignKey('office.id'), nullable=False)
  status = Column(Enum('pending', 'confirmed', 'cancelled', 'completed', name="status"), nullable=False)
  
  num_tarjeta = Column(String(16), nullable = False)
  
  booking_date = Column(TIMESTAMP(timezone=True), server_default=func.now())
  pickUp_date = Column(DateTime, nullable=False)
  return_date = Column(DateTime, nullable=False)
  price = Column(DECIMAL(10,2))  

  #Aniado de momento los siguientes:
  reserva_tiene_estado = relationship("Estado_reserva", back_populates="estado_tiene_reserva")
  reserva_realiza_usuario = relationship("Usuario", back_populates="usuario_realiza_reserva")

  __table_args__ = (
        CheckConstraint("LENGTH(num_tarjeta) = 16 AND num_tarjeta ~ '^[0-9]+$'", name="num_tarjeta_valida"),
    )

class Documento_pago (Base):
  __tablename__ = 'documento_pago'
  id_documento = Column(Integer, primary_key=True, nullable=False)
  num_tarjeta_docs = Column(String(16), nullable=False)
  forma_de_pago = Column(String(50), nullable=False)
  importe = Column(Double, nullable=False)
  
class Calculado 

class Estado_reserva (Base):
  __tablename__ = 'estado_reserva'
  id_estado = Column(Enum('en_curso', 'pendiente', 'modificada', 'cancelada', 'finalizada'), primary_key=True, nullable=False)
  fecha = Column(DateTime, nullable=False)

  tiene_estado_reserva = Column(Integer, ForeignKey('reserva.n_reserva')) #Nullable=false?

  estado_tiene_reserva = relationship("Reserva", back_populates="reserva_tiene_estado")

class Coche (Base):
  __tablename__= 'coche'
  id_coche = Column(Integer, primary_key=True, nullable=False )
  tipo_cambio = Column(Enum('a', 'm'))
  puertas = Column(Integer)
  techo_solar = Column(Boolean)

  c_es_m = Column(String(100), ForeignKey("modelo.modelo"), nullable=False)

  coche_con_modelo = relationship("Modelo", back_populates="modelo_de_coche")
  estados = relationship("Estados_coche", back_populates="coche_estado")
  ubicaciones = relationship("UbicadoEn", back_populates="coche_ubi")

class Estado_coche (Base):
  __tablename__= 'estado_coche'
  fecha_desde = Column(DateTime, primary_key=True, nullable=False)
  fecha_hasta = Column(DateTime) #comprobar después si puede no ser null
  estado = Column(Enum('ocupado', 'libre'))

  coche_id = Column(Integer, ForeignKey('coche.id_coche'), nullable=False)

  coche_estado = relationship("Coche", back_populates="estados")

#tabla de asosiacion modelo-tarifa
modelo_tarifa = Table("modelo_tarifa", 
                      Base.metadata,
                      Column( 'modelo', String(100), ForeignKey('modelo.modelo'), primary_key=True),
                      Column( 'id_tarifa', Integer, ForeignKey('tarifa.id_tarifa'), primary_key=True))

class Modelo (Base):
  __tablename__= 'modelo'
  #dejar como key solo a marca?? 
  modelo = Column(String(100), primary_key=True, nullable=False)
  marca = Column(String(100), nullable=False)
  categoria_precio = Column(Enum('gama_alta', 'media', 'baja'), nullable=False)

  modelo_de_coche = relationship("Coche", back_populates="coche_con_modelo")
  modelo_tiene_tarifa = relationship("Tarifa", secondary=modelo_tarifa, back_populates="tarifa_tiene_modelo")

class Tarifa (Base):
  __tablename__ = 'tarifa'

  id_tarifa = Column(Integer, primary_key=True, nullable=False)

  tarifa_tiene_modelo = relationship("Modelo", secondary=modelo_tarifa, back_populates="modelo_tiene_tarifa")

  
