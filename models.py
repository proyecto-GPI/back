# models.py

from sqlalchemy import String, Integer, Column, ForeignKey, Enum, TIMESTAMP, DateTime, CheckConstraint, DECIMAL, Text, Boolean, Table, Double, Float, Date, PrimaryKeyConstraint, ForeignKeyConstraint, Index, Numeric
from database import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


#tabla de asosiacion entre descuento y usuario <-> relacion m2m (many to many)
# REVISAR si este tipo de estrucutras es correcta 
descuento_usuario = Table("descuento_usuario", 
                      Base.metadata,
                      Column( 'id_usuario', String(9), ForeignKey('usuario.id'), primary_key=True),
                      Column( 'codigo', String(10), ForeignKey('descuento.codigo'), primary_key=True))


class Usuario (Base):
  __tablename__= 'usuario'
  # the id will be the DNI of the user
  id = Column(String(9), primary_key=True, nullable=False)
  correo = Column(String(255), nullable=False, unique=True)
  nombre = Column(String(255), nullable=False)
  contrasenya = Column(String(64), nullable=False)
  tipo_cliente = Column(Enum('negocio', 'particular', 'admin', name="tipo_cliente"), nullable=False)
  fecha_registro = Column(Date, nullable=False)
  
  usuario_realiza_reserva = relationship("Reserva", back_populates="reserva_realiza_usuario")
  usuario_tiene_asignado_descuento = relationship("Descuento", secondary=descuento_usuario, back_populates="descuento_tiene_asignado_usuario")

#relacion m2m entre descuento y documento de pago
descuento_documento_pago = Table("descuento_documento_pago", 
                      Base.metadata,
                      Column( 'id_documento', Integer, ForeignKey('documento_pago.id_documento'), primary_key=True),
                      Column( 'codigo', String(10), ForeignKey('descuento.codigo'), primary_key=True))


#relacion m2m entre  modelo y tarifa 
modelo_tarifa = Table(
    "modelo_tarifa", Base.metadata,
    Column("modelo", String(80), primary_key=True),
    Column("categoria", Enum("alta", "media", "baja", name="categoria"), primary_key=True),
    Column("id_tarifa", Integer, ForeignKey("tarifa.id_tarifa"), primary_key=True),
    ForeignKeyConstraint(
        ["modelo", "categoria"],
        ["modelo.modelo", "modelo.categoria"],
        name="fk_modelo_tarifa_modelo"
    )
)

class Modelo (Base):
  __tablename__= 'modelo'
  modelo = Column(String(80), nullable=False)
  marca = Column(String(45), nullable=False)
  categoria = Column(Enum('alta', 'media', 'baja', name = "categoria"), nullable=False)
  
  # definimos la primary key compuesta
  __table_args__ = (
       PrimaryKeyConstraint('modelo', 'categoria'),
   )

  modelo_es_coche = relationship("Coche", back_populates="coche_es_modelo")
  modelo_tiene_tarifa = relationship("Tarifa", secondary=modelo_tarifa, back_populates="tarifa_tiene_modelo")


class Coche (Base):
  __tablename__= 'coche'
  id = Column(Integer, primary_key=True, nullable=False)
  techo_solar = Column(Boolean, nullable=False)
  puertas = Column(Integer, nullable=False)
  tipo_cambio = Column(Enum('a', 'm', name = "tipo_cambio"), nullable=False)

  modelo = Column(String(80), nullable=False)
  categoria = Column(Enum('alta', 'media', 'baja', name = "categoria"), nullable=False)
 
  # definimos la foreign key y el index
  __table_args__ = (
      ForeignKeyConstraint(
          ['modelo', 'categoria'],
          ['modelo.modelo', 'modelo.categoria'],
          name = 'fk_coche_modelo1',
          ondelete='NO ACTION',
          onupdate= 'NO ACTION'          
          ),
      Index('fk_coche_modelo1_idx', 'modelo', 'categoria', unique=False)
  )

  coche_es_modelo = relationship("Modelo", back_populates="modelo_es_coche")
  coche_tiene_estado_coche = relationship("Estado_coche", back_populates="estado_coche_tiene_coche")

  
  coche_tiene_reserva = relationship("Reserva", back_populates="reserva_tiene_coche")
  ubicaciones = relationship("UbicadoEn", back_populates="coche_ubi")
  




class Oficina(Base):
  __tablename__= 'oficina'
  id_oficina = Column(Integer, primary_key=True, nullable=False)
  direccion = Column(String(512), nullable=False, unique=True)
  nombre = Column(String(80), nullable=False)
  ciudad = Column(String(80), nullable=False)

  ubicaciones = relationship("UbicadoEn", back_populates="oficina")
  oficina_pagado_en_documento_pago = relationship("Documento_pago", back_populates="documento_pago_pagado_en_oficina")
  oficina_recoge_reserva = relationship(
      "Reserva",
      back_populates="reserva_recoge_oficina",
      foreign_keys="[Reserva.id_oficina_recogida_real]"
  )

  oficina_devuelve_reserva = relationship(
      "Reserva",
      back_populates="reserva_devuelve_oficina",
      foreign_keys="[Reserva.id_oficina_devolucion_real]"
  )



#relacion m2m entre extra y reserva
extra_reserva = Table("extra_reserva", 
                      Base.metadata,
                      Column( 'id_extra', Integer, ForeignKey('extra.id_extra'), primary_key=True),
                      Column( 'id_reserva', Integer, ForeignKey('reserva.id_reserva'), primary_key=True))

#NO esta completada del todo-----------------------------------------
class Reserva(Base):
  __tablename__= 'reserva'
  id_reserva=Column(Integer, primary_key=True, nullable=False)
  oficina_recogida_propuesta = Column(Integer,  nullable=False)
  oficina_devolucion_propuesta = Column(Integer, nullable=False)
  fecha_recogida_propuesta = Column(Date, nullable=False)
  fecha_devolucion_propuesta = Column(Date, nullable=False)
  fecha_confirmacion = Column(Date, nullable=False)
  importe_final_previsto = Column(Numeric(10,2), nullable=False)
  num_tarjeta = Column(String(16), nullable = False)
  fecha_recogida_real = Column(Date)
  fecha_devolucion_real = Column(Date)
  id_usuario = Column(String(9), ForeignKey('usuario.id', ondelete='NO ACTION', onupdate='NO ACTION'), nullable=False)
  reserva_realiza_usuario = relationship("Usuario", back_populates="usuario_realiza_reserva")
  id_coche = Column( Integer,  ForeignKey('coche.id', ondelete='NO ACTION', onupdate='NO ACTION'), nullable=False)
  reserva_tiene_coche = relationship("Coche", back_populates="coche_tiene_reserva")
  id_oficina_recogida_real = Column(
    Integer,
    ForeignKey('oficina.id_oficina', ondelete='NO ACTION', onupdate='NO ACTION')
  )
  id_oficina_devolucion_real = Column(
    Integer,
    ForeignKey('oficina.id_oficina', ondelete='NO ACTION', onupdate='NO ACTION')
  )
  reserva_recoge_oficina = relationship(
    "Oficina",
    back_populates="oficina_recoge_reserva",
    foreign_keys=[id_oficina_recogida_real]
  )

  reserva_devuelve_oficina = relationship(
      "Oficina",
      back_populates="oficina_devuelve_reserva",
      foreign_keys=[id_oficina_devolucion_real]
  )

  reserva_finaliza_y_genera_documento_pago = relationship("Documento_pago", back_populates="documento_pago_finaliza_y_genera_reserva")

  reserva_tiene_estado = relationship("Estado_reserva", back_populates="estado_tiene_reserva")

  reserva_tiene_extra = relationship(
    "Extra",
    secondary=extra_reserva,
    back_populates="extra_tiene_reserva"
  )

  reserva_tiene_descuento = relationship("Descuento", back_populates="descuento_tiene_reserva")

  id_reserva_padre = Column(
    Integer,
    ForeignKey('reserva.id_reserva', ondelete='NO ACTION', onupdate='NO ACTION'),
    nullable=True
  )

  reserva_padre = relationship("Reserva", remote_side="Reserva.id_reserva")









  
  
# id_tarifa = Column(Integer, ForeignKey('tarifa.id_tarifa'), nullable=False) # revisar si es necesario o no

id_oficina_recogida_real = Column(
    Integer, 
    ForeignKey('oficina.id_oficina', ondelete='NO ACTION', onupdate='NO ACTION')
)

id_oficina_devolucion_real = Column(
    Integer, 
    ForeignKey('oficina.id_oficina', ondelete='NO ACTION', onupdate='NO ACTION')
)

id_coche = Column(
    Integer, 
    ForeignKey('coche.id', ondelete='NO ACTION', onupdate='NO ACTION'),
    nullable=False
)

id_reserva_padre = Column(
    Integer, 
    ForeignKey('reserva.id_reserva', ondelete='NO ACTION', onupdate='NO ACTION')
)


#cosas de antes por corregir y/o descartar -------
  #n_plate = Column(String(15), ForeignKey('car.n_plate'), nullable=False)
  #budget_id = Column(Integer, ForeignKey(budget.id), nullable=False)
  #status = Column(Enum('pending', 'confirmed', 'cancelled', 'completed', name="status"), nullable=False)
  #booking_date = Column(TIMESTAMP(timezone=True), server_default=func.now())
  #pickUp_date = Column(DateTime, nullable=False)
  #return_date = Column(DateTime, nullable=False)
  #price = Column(DECIMAL(10,2))  
#fin-------------------------------

  # index y validacion tarjeta
_table_args__ = (
    Index('fk_reserva_usuario1_idx', 'id_usuario'),
    Index('fk_reserva_oficina1_idx', 'id_oficina_recogida_real'),
    Index('fk_reserva_oficina2_idx', 'id_oficina_devolucion_real'),
    Index('fk_reserva_coche1_idx', 'id_coche'),
    Index('fk_reserva_reserva1_idx', 'id_reserva_padre'),
    
    CheckConstraint("LENGTH(num_tarjeta) = 16 AND num_tarjeta ~ '^[0-9]+$'", name="num_tarjeta_valida"),
)

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
#reserva_modificada = relationship("Reserva", remote_side=[id_reserva], backref="modifica_y_genera") #RESVISAR, si es correcto TODO: solucionar


class Tarifa (Base):
  __tablename__ = 'tarifa'

  id_tarifa = Column(Integer, primary_key=True, nullable=False)
  tipo_tarifa = Column(Enum('dia_km', 'km', 'dia', 'semana', 'fin_semana', name = "tipo_tarifa"), nullable=False)

  tarifa_tiene_modelo = relationship("Modelo", secondary=modelo_tarifa, back_populates="modelo_tiene_tarifa")
  calculado_por = relationship("CalculadoPor", back_populates="tarifa")

  


class Tarifa_cd (Base):
  __tablename__ = 'tarifa_cd'
  
  id_tarifa = Column(Integer, nullable=False)  
  tipo_tarifa_cd = Column(Enum('dia_km', 'km', 'dia', 'semana', 'fin_semana', name = "tipo_tarifa_cd" ), nullable=False)  
  precio = Column(Numeric(10, 2), nullable=False)
  periodo = Column(Enum('1', '2', '3', name = "periodo"), nullable=False)
  
  __table_args__ = (
       PrimaryKeyConstraint('id_tarifa', 'periodo'),
       ForeignKeyConstraint(
           ['id_tarifa'],
           ['tarifa.id_tarifa'],
           ondelete='NO ACTION',
           onupdate='NO ACTION'
       )
   )


class Estado_coche (Base):
  __tablename__= 'estado_coche'
  fecha_desde = Column(DateTime, nullable=False)
  fecha_hasta = Column(DateTime)
  libre = Column(Boolean, nullable=False)

  id_coche = Column(Integer, ForeignKey('coche.id', ondelete='NO ACTION', onupdate='NO ACTION'), nullable=False)

  __table_args__ = (
       PrimaryKeyConstraint('id_coche', 'fecha_desde'),
       
       Index('fk_estado_coche_coche1_idx', 'id_coche'),
   )


  estado_coche_tiene_coche = relationship("Coche", back_populates="coche_tiene_estado_coche")


class Tarifa_ld (Base):
  __tablename__ = 'tarifa_ld'
  
  id_tarifa = Column(Integer, ForeignKey('tarifa.id_tarifa', ondelete='NO ACTION', onupdate='NO ACTION'), primary_key=True, nullable=False)  
  precio = Column(Numeric(10, 2), nullable=False)
  




#relacion m2m entre documento de pago y extra
documento_pago_extra = Table("documento_pago_extra", 
                      Base.metadata,
                      Column( 'id_documento', Integer, ForeignKey('documento_pago.id_documento'), primary_key=True),
                      Column( 'id_extra', Integer, ForeignKey('extra.id_extra'), primary_key=True))


class Documento_pago (Base):
  __tablename__ = 'documento_pago'

  id_documento = Column(Integer, primary_key=True, nullable=False)
  id_reserva = Column(Integer,ForeignKey('reserva.id_reserva', onupdate='NO ACTION', ondelete='NO ACTION'), nullable=False)
  num_tarjeta = Column(String(16), nullable=False)
  forma_pago = Column(Enum('efectivo', 'tarjeta', name = "forma_pago"), nullable=False)
  importe = Column(Numeric(10,2), nullable=False)
 


  id_oficina = Column(
    Integer, 
    ForeignKey('oficina.id_oficina', ondelete='NO ACTION', onupdate='NO ACTION'), 
    nullable=False
  )

  __table_args__ = (
       Index('fk_documento_pago_reserva1_idx', 'id_reserva'),
       Index('fk_documento_pago_oficina1_idx', 'id_oficina')
   )

  calculado_por = relationship("CalculadoPor", back_populates="documento_pago")
  documento_pago_aplicado_a_descuento = relationship("Descuento", secondary=descuento_documento_pago, back_populates="descuento_aplicado_a_documento_pago")
  documento_pago_contiene_extra = relationship("Extra", secondary=documento_pago_extra, back_populates="extra_contiene_documento_pago")
  documento_pago_pagado_en_oficina = relationship("Oficina", back_populates="oficina_pagado_en_documento_pago")
  documento_pago_finaliza_y_genera_reserva = relationship("Reserva", back_populates="reserva_finaliza_y_genera_documento_pago")
  calculado_por = relationship("CalculadoPor", back_populates="documento_pago")


class Estado_reserva (Base):
  __tablename__ = 'estado_reserva'
  id_estado = Column(Enum('en_curso', 'pendiente', 'modificada', 'cancelada', 'finalizada', name = "id_estado"), nullable=False)
  fecha_desde = Column(DateTime, nullable=False)

  id_reserva = Column(Integer, ForeignKey('reserva.id_reserva', ondelete='NO ACTION', onupdate='NO ACTION'), nullable=False) 
  __table_args__ = (
       PrimaryKeyConstraint('id_reserva', 'id_estado'),
       
       Index('fk_estado_reserva_reserva1_idx', 'id_reserva' )
   )


  estado_tiene_reserva = relationship("Reserva", back_populates="reserva_tiene_estado")




class Extra (Base):
  __tablename__ = 'extra'

  id_extra = Column(Integer, primary_key=True, nullable=False)
  descripcion = Column(String(45), nullable=False, unique=True)
    
  # revisar estas relaciones, he quitado un atributo de arriba
  extra_historico_precio = relationship("Historico_precio", back_populates="historico_precio_extra")
  extra_tiene_reserva = relationship("Reserva", secondary=extra_reserva, back_populates="reserva_tiene_extra")
  extra_contiene_documento_pago = relationship("Documento_pago", secondary=documento_pago_extra, back_populates="documento_pago_contiene_extra")
  



class Historico_precio (Base):
  __tablename__ = 'historico_precio'

  fecha_establecido = Column(DateTime, nullable=False)
  precio = Column(Numeric(10,2), nullable=False)
  id_extra = Column(
    Integer,
    ForeignKey('extra.id_extra', ondelete='NO ACTION', onupdate='NO ACTION'),
    nullable=False
)

  
  __table_args__ = (
     PrimaryKeyConstraint('fecha_establecido', 'id_extra'),
     Index('fk_historico_precio_extra1_idx', 'id_extra')
 )


  historico_precio_extra = relationship("Extra", back_populates="extra_historico_precio")
 
  
class Descuento (Base):
   __tablename__ = 'descuento'

   codigo = Column(String(10), primary_key=True, nullable=False) 
   caducidad = Column(Date)
   porcentaje = Column(Integer, nullable=False )

   id_reserva = Column(
    Integer,
    ForeignKey('reserva.id_reserva', ondelete='NO ACTION', onupdate='NO ACTION'),
    nullable=False
  )


   __table_args__ = (
       Index('fk_descuento_reserva1_idx', 'id_reserva'),
       )

   descuento_tiene_reserva = relationship("Reserva", back_populates="reserva_tiene_descuento")
   descuento_tiene_asignado_usuario = relationship("Usuario", secondary=descuento_usuario, back_populates="usuario_tiene_asignado_descuento")
   descuento_aplicado_a_documento_pago = relationship("Documento_pago", secondary=descuento_documento_pago, back_populates="documento_pago_aplicado_a_descuento")



#############mark#################


#Para relaciones con atributo (# REVISAR si este tipo de estrucutras es correcta )
class UbicadoEn(Base):
  __tablename__ = 'coche_en_oficina'

  fecha_hasta = Column(DateTime, primary_key=True, nullable=False)
  fecha_desde = Column(DateTime)
  
  id_coche = Column(Integer, ForeignKey("coche.id"), primary_key=True, nullable=False)  
  id_oficina = Column(Integer, ForeignKey("oficina.id_oficina"), primary_key=True, nullable=False) 
  
  coche_ubi = relationship("Coche", back_populates="ubicaciones")
  oficina = relationship("Oficina", back_populates="ubicaciones")
  




  

#Para relaciones con atributo  
class CalculadoPor (Base):
  __tablename__ =  'calculado_por'

  id_tarifa = Column(Integer, ForeignKey("tarifa.id_tarifa"), primary_key=True)
  id_documento = Column(Integer, ForeignKey("documento_pago.id_documento"), primary_key=True)
  volumen = Column(Integer) #REVISAR, no se que tipo es

  tarifa = relationship("Tarifa", back_populates="calculado_por")
  documento_pago = relationship("Documento_pago", back_populates="calculado_por")




