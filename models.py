# models.py

from sqlalchemy import String, Integer, Column, ForeignKey, Enum, TIMESTAMP, DateTime, CheckConstraint, DECIMAL, Text, Boolean, Table, Double, Float
from database import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship





class Oficina(Base):
  __tablename__= 'oficina'
  id_oficina = Column(Integer, primary_key=True, nullable=False)
  direccion = Column(String(50))
  #should we include the schedule?
  #schedule = Column(String(20))

  ubicado_en = relationship("UbicadoEn", back_populates="oficina")
  oficina_recoge_reserva = relationship("Reserva", back_populates="reserva_recoge_oficina")
  oficina_devuelve_reserva = relationship("Reserva", back_populates="reserva_devuelve_oficina")
  oficina_pagado_en_documento_pago = relationship("Documento_pago", back_populates="documento_pago_pagado_en_oficina")

#Para relaciones con atributo (# REVISAR si este tipo de estrucutras es correcta )
class UbicadoEn(Base):
  __tablename__ = 'ubicado_en'

  fecha_hasta = Column(DateTime, primary_key=True, nullable=False)
  fecha_desde = Column(DateTime)
  
  coche_id = Column(Integer, ForeignKey("coche.id_coche"), nullable=False)  
  oficina_id = Column(Integer, ForeignKey("oficina.id_oficina"), nullable=False) 
  
  coche_ubi = relationship("Coche", back_populates="ubicaciones")
  oficina = relationship("Oficina", back_populates="ubicaciones")
  

#tabla de asosiacion entre descuento y usuario <-> relacion m2m (many to many)
# REVISAR si este tipo de estrucutras es correcta 
descuento_usuario = Table("descuento_usuario", 
                      Base.metadata,
                      Column( 'DNI_usuario', String(9), ForeignKey('usuario.DNI_usuario'), primary_key=True),
                      Column( 'cod_descuento', String(15), ForeignKey('descuento.cod_descuento'), primary_key=True))


class Usuario (Base):
  __tablename__= 'usuario'
  # the id will be the DNI of the user
  DNI_usuario=Column(String(9), primary_key=True, nullable=False)
  nombre = Column(String(20))
  correo = Column(String(20))
  contrasenia = Column(Text, nullable=False)
  tipo_cliente = Column(Enum('individual', 'business', name="customer_type"), nullable=True)
  # esperar a ver que enumerados se ponen en el paso a tablas?

  usuario_realiza_reserva = relationship("Reserva", back_populates="reserva_realiza_usuario")
  usuario_tiene_asignado_descuento = relationship("Descuento", secondary=descuento_usuario, back_populates="descuento_tiene_asignado_usuario")

#relacion m2m entre descuento y documento de pago
descuento_documento_pago = Table("descunto_documento_pago", 
                      Base.metadata,
                      Column( 'id_documento', Integer, ForeignKey('documento_pago.id_documento'), primary_key=True),
                      Column( 'cod_descuento', String(15), ForeignKey('descuento.cod_descuento'), primary_key=True))

class Descuento (Base):
  __tablename__ = 'descuento'

  cod_descuento = Column(String(15), primary_key=True, nullable=False) #longitud entre 8 y 12
  porcentaje = Column(Float, nullable=False ) #REVISAR, estoy suponiendo el tipo Float
  condiciones = Column(String(500))

  n_reserva = Column(Integer, ForeignKey('reserva.n_reserva'), nullable=False)

  descuento_tiene_reserva = relationship("Reserva", back_populates="reserva_tiene_descuento")
  descuento_tiene_asignado_usuario = relationship("Usuario", secondary=descuento_usuario, back_populates="usuario_tiene_asignado_descuento")
  descuento_aplicado_a_documento_pago = relationship("Documento_pago", secondary=descuento_documento_pago, back_populates="documento_pago_aplicado_a_descuento")


  
#relacion m2m entre extra y reserva
extra_reserva = Table("extra_reserva", 
                      Base.metadata,
                      Column( 'codigo_extra', String(15), ForeignKey('extra.codigo_extra'), primary_key=True),
                      Column( 'n_reserva', Integer, ForeignKey('reserva.n_reserva'), primary_key=True))

#NO esta completada del todo-----------------------------------------
class Reserva (Base):
  __tablename__= 'reserva'
  n_reserva=Column(Integer, primary_key=True, nullable=False)
  num_tarjeta = Column(String(16), nullable = False)

  DNI_usuario = Column(String(9), ForeignKey('usuario.DNI_usuario'), nullable=False)
  id_tarifa = Column(Integer, ForeignKey('tarifa. id_tarifa'), nullable=False)
  id_oficina_recoge = Column(Integer, ForeignKey('oficina.id_oficina'), nullable=False)
  id_oficina_devuelve = Column(Integer, ForeignKey('oficina.id_oficina'), nullable=False)
  id_coche = Column(Integer, ForeignKey('coche.id_coche'), nullable=False) 
  n_reserva_modificada = Column(Integer, ForeignKey('reserva.n_reserva'), nullable=True)

#cosas de antes por corregir y/o descartar -------
  #n_plate = Column(String(15), ForeignKey('car.n_plate'), nullable=False)
  #budget_id = Column(Integer, ForeignKey(budget.id), nullable=False)
  #status = Column(Enum('pending', 'confirmed', 'cancelled', 'completed', name="status"), nullable=False)
  #booking_date = Column(TIMESTAMP(timezone=True), server_default=func.now())
  #pickUp_date = Column(DateTime, nullable=False)
  #return_date = Column(DateTime, nullable=False)
  #price = Column(DECIMAL(10,2))  
#fin-------------------------------

  #Aniado de momento los siguientes:
  reserva_tiene_estado = relationship("Estado_reserva", back_populates="estado_tiene_reserva")
  reserva_realiza_usuario = relationship("Usuario", back_populates="usuario_realiza_reserva")
  reserva_tiene_tarifa = relationship("Tarifa", back_populates="tarifa_tiene_reserva")
  reserva_tiene_descuento = relationship("Descuento", back_populates="descuento_tiene_reserva")
  reserva_tiene_extra = relationship("Extra", secondary=extra_reserva, back_populates="extra_tiene_reserva")
  reserva_recoge_oficina = relationship("Oficina", back_populates="oficina_recoge_reserva")
  reserva_devuelve_oficina = relationship("Oficina", back_populates="oficina_devuelve_reserva")
  reserva_finaliza_y_genera_documento_pago = relationship("Documento_pago", back_populates="documento_pago_finaliza_y_genera_reserva")
  reserva_tiene_coche = relationship("Coche", back_populates="coche_tiene_reserva")
  reserva_modificada = relationship("Reserva", remote_side=[n_reserva], backref="modifica_y_genera") #RESVISAR, si es correcto

  __table_args__ = (
        CheckConstraint("LENGTH(num_tarjeta) = 16 AND num_tarjeta ~ '^[0-9]+$'", name="num_tarjeta_valida"),
    )

#relacion m2m entre documento de pago y extra
documento_pago_extra = Table("documento_pago_extra", 
                      Base.metadata,
                      Column( 'id_documento', Integer, ForeignKey('documento_pago.id_documento'), primary_key=True),
                      Column( 'codigo_extra', String(15), ForeignKey('extra.codigo_extra'), primary_key=True))


class Documento_pago (Base):
  __tablename__ = 'documento_pago'

  id_documento = Column(Integer, primary_key=True, nullable=False)
  num_tarjeta_docs = Column(String(16), nullable=False)
  forma_de_pago = Column(String(50), nullable=False)
  importe = Column(Float, nullable=False)

  id_oficina = Column(Integer, ForeignKey('oficina.id_oficina'), nullable=False)

  calculado_por = relationship("CalculadoPor", back_populates="documento_pago")
  documento_pago_aplicado_a_descuento = relationship("Descuento", secondary=descuento_documento_pago, back_populates="descuento_aplicado_a_documento_pago")
  documento_pago_contiene_extra = relationship("Extra", secondary=documento_pago_extra, back_populates="extra_contiene_documento_pago")
  documento_pago_pagado_en_oficina = relationship("Oficina", back_populates="oficina_pagado_en_documento_pago")
  documento_pago_finaliza_y_genera_reserva = relationship("Reserva", back_populates="reserva_finaliza_y_genera_documento_pago")

#Para relaciones con atributo  
class CalculadoPor (Base):
  __tablename__ =  'calculado_por'

  id_tarifa = Column(Integer, ForeignKey("tarifa.id_tarifa"), primary_key=True)
  id_documento = Column(Integer, ForeignKey("documento_pago.id_documento"), primary_key=True)
  volumen = Column(Integer) #REVISAR, no se que tipo es

  tarifa = relationship("Tarifa", back_populates="calculado_por")
  documento_pago = relationship("DocumentoPago", back_populates="calculado_por")


class Estado_reserva (Base):
  __tablename__ = 'estado_reserva'
  id_estado = Column(Enum('en_curso', 'pendiente', 'modificada', 'cancelada', 'finalizada'), primary_key=True, nullable=False)
  fecha = Column(DateTime, nullable=False)

  n_reserva = Column(Integer, ForeignKey('reserva.n_reserva')) #Nullable=false?

  estado_tiene_reserva = relationship("Reserva", back_populates="reserva_tiene_estado")

class Coche (Base):
  __tablename__= 'coche'
  id_coche = Column(Integer, primary_key=True, nullable=False )
  tipo_cambio = Column(Enum('a', 'm'))
  puertas = Column(Integer)
  techo_solar = Column(Boolean)

  modelo = Column(String(100), ForeignKey("modelo.modelo"), nullable=False)

  coche_es_modelo = relationship("Modelo", back_populates="modelo_es_coche")
  coche_tiene_estado_coche = relationship("Estados_coche", back_populates="estado_coche_tiene_coche")
  ubicado_en = relationship("UbicadoEn", back_populates="coche_ubi")
  coche_tiene_reserva = relationship("Reserva", back_populates="reserva_tiene_coche")

class Estado_coche (Base):
  __tablename__= 'estado_coche'
  fecha_desde = Column(DateTime, primary_key=True, nullable=False)
  fecha_hasta = Column(DateTime) #comprobar después si puede no ser null
  estado = Column(Enum('ocupado', 'libre'))

  id_coche = Column(Integer, ForeignKey('coche.id_coche'), nullable=False)

  estado_coche_tiene_coche = relationship("Coche", back_populates="coche_tiene_estado_coche")

#relacion m2m entre  modelo y tarifa 
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

  modelo_es_coche = relationship("Coche", back_populates="coche_es_modelo")
  modelo_tiene_tarifa = relationship("Tarifa", secondary=modelo_tarifa, back_populates="tarifa_tiene_modelo")

class Tarifa (Base):
  __tablename__ = 'tarifa'

  id_tarifa = Column(Integer, primary_key=True, nullable=False)

  tarifa_tiene_modelo = relationship("Modelo", secondary=modelo_tarifa, back_populates="modelo_tiene_tarifa")
  calculado_por = relationship("CalculadoPor", back_populates="tarifa")
  tarifa_tiene_reserva  =relationship("reserva", back_populates="reserva_tiene_tarifa")
  
class Extra (Base):
  __tablename__ = 'extra'

  codigo_extra = Column(String(15), primary_key=True, nullable=False)#REVISAR, estoy suponiendo este limite de string y el tipo
  descripcion = Column(String(500))

  extra_historico_precio = relationship("Historico_precio", back_populates="historico_precio_extra")
  extra_tiene_reserva = relationship("Reserva", secondary=extra_reserva, back_populates="reserva_tiene_extra")
  extra_contiene_documento_pago = relationship("Documento_pago", secondary=documento_pago_extra, back_populates="documento_pago_contiene_extra")

class Historico_precio (Base):
  __tablename__ = 'historico_precio'

  fecha_establecido = Column(DateTime, primary_key=True, nullable=False)
  precio = Column(Float)

  codigo_extra = Column(String(15), ForeignKey('extra.codigo_extra'), nullable=False)

  historico_precio_extra = relationship("Extra", back_populates="extra_historico_precio")