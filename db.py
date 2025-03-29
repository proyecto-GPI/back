#db.py
import psycopg2
"""
--Instructions to create the user in the database named 'autoveloz'

CREATE USER autoveloz_creator WITH ENCRYPTED PASSWORD 'autovelozGPI';
ALTER DATABASE autoveloz OWNER TO autoveloz_creator;
GRANT ALL PRIVILEGES ON SCHEMA public TO autoveloz_creator;

"""


# new conn to db
conn = psycopg2.connect(host = "localhost", dbname="autoveloz", user="autoveloz_creator", password="autovelozGPI", port=5432)

cur = conn.cursor()


# definimos los ENUM necesarios
cur.execute("CREATE TYPE categoria AS ENUM('alta', 'media', 'baja')")
cur.execute("CREATE TYPE tipo_cliente AS ENUM('negocio', 'particular', 'admin')")
cur.execute("CREATE TYPE tipo_cambio AS ENUM('m', 'a')")
cur.execute("CREATE TYPE tipo_tarifa AS ENUM('tarifa_cd', 'tarifa_ld')")
cur.execute("CREATE TYPE tipo_tarifa_cd AS ENUM('dia_km', 'km', 'dia', 'semana', 'fin_semana')")
cur.execute("CREATE TYPE periodo AS ENUM('1', '2', '3')")
cur.execute("CREATE TYPE forma_pago AS ENUM('efectivo', 'tarjeta')")
cur.execute("CREATE TYPE estado AS ENUM('pendiente', 'en_curso', 'finalizada', 'modificada', 'cancelada') ")



# creamos las tablas necesarias
tables_statement = """

-- usuario
CREATE TABLE IF NOT EXISTS usuario (
   id CHAR(9) PRIMARY KEY,
   correo VARCHAR(255) NOT NULL UNIQUE,
   nombre VARCHAR(255) NOT NULL,
   contrasenya VARCHAR(64) NOT NULL,
   tipo_cliente tipo_cliente NOT NULL,
   fecha_registro DATE NOT NULL
);

COMMENT ON COLUMN usuario.id IS 'DNI o NIF';


-- modelo
CREATE TABLE IF NOT EXISTS modelo (
   modelo VARCHAR(80) NOT NULL,
   categoria categoria NOT NULL,
   marca VARCHAR(45) NOT NULL,
   PRIMARY KEY (modelo, categoria)
);


-- coche
CREATE TABLE IF NOT EXISTS coche (
   id SERIAL PRIMARY KEY,
   techo_solar BOOLEAN NOT NULL,
   puertas INT NOT NULL,
   tipo_cambio tipo_cambio NOT NULL,
   modelo VARCHAR(80) NOT NULL,
   categoria categoria NOT NULL,
   CONSTRAINT fk_coche_modelo1
      FOREIGN KEY (modelo, categoria)
      REFERENCES modelo (modelo, categoria)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION
);

CREATE INDEX fk_coche_modelo1_idx ON coche (modelo ASC, categoria ASC);

COMMENT ON COLUMN coche.id IS 'Identificador del coche que se autoincrementa cada vez que creamos una instancia de la entidad nueva';

COMMENT ON COLUMN coche.tipo_cambio IS '1 si libre. 0 si ocupado';


-- oficina
CREATE TABLE IF NOT EXISTS oficina (
   id_oficina SERIAL PRIMARY KEY,
   direccion  VARCHAR(512) NOT NULL UNIQUE
);
 

-- reserva
CREATE TABLE IF NOT EXISTS reserva (
   id_reserva SERIAL PRIMARY KEY,
   oficina_recogida_propuesta INT NOT NULL,
   oficina_devolucion_propuesta INT NOT NULL,
   fecha_recogida_propuesta DATE NOT NULL,
   fecha_devolucion_propuesta DATE NOT NULL,
   fecha_confirmacion DATE NOT NULL,
   importe_final_previsto DECIMAL(10,2) NOT NULL,
   num_tarjeta VARCHAR(16) NOT NULL CHECK (LENGTH(num_tarjeta) = 16 AND num_tarjeta ~ '^[0-9]+$'),
   fecha_recogida_real DATE NULL,
   fecha_devolucion_real DATE NULL,
   id_usuario CHAR(9) NOT NULL,
   id_oficina_recogida_real INT NULL,
   id_oficina_devolucion_real INT NULL,
   id_coche INT NOT NULL,
   id_reserva_padre INT NULL,
   CONSTRAINT fk_reserva_usuario1
     FOREIGN KEY (id_usuario)
     REFERENCES usuario(id)
     ON DELETE NO ACTION
     ON UPDATE NO ACTION,
   CONSTRAINT fk_reserva_oficina1
     FOREIGN KEY (id_oficina_recogida_real)
     REFERENCES oficina(id_oficina)
     ON DELETE NO ACTION
     ON UPDATE NO ACTION,
   CONSTRAINT fk_reserva_oficina2
     FOREIGN KEY (id_oficina_devolucion_real)
     REFERENCES oficina(id_oficina)
     ON DELETE NO ACTION
     ON UPDATE NO ACTION,
   CONSTRAINT fk_reserva_coche1
     FOREIGN KEY (id_coche)
     REFERENCES coche(id)
     ON DELETE NO ACTION
     ON UPDATE NO ACTION,
   CONSTRAINT fk_reserva_reserva1
     FOREIGN KEY (id_reserva_padre)
     REFERENCES reserva(id_reserva)
     ON DELETE NO ACTION
     ON UPDATE NO ACTION
);

CREATE INDEX fk_reserva_usuario1_idx ON reserva (id_usuario ASC);

CREATE INDEX fk_reserva_oficina1_idx ON reserva (id_oficina_recogida_real ASC);

CREATE INDEX fk_reserva_oficina2_idx ON reserva (id_oficina_devolucion_real ASC);

CREATE INDEX fk_reserva_coche1_idx ON reserva (id_coche ASC);

CREATE INDEX fk_reserva_reserva1_idx ON reserva (id_reserva_padre ASC);

COMMENT ON COLUMN reserva.id_reserva IS 'Autoincremental';

COMMENT ON COLUMN reserva.oficina_recogida_propuesta IS 'Direccion de la oficina de recogida. Apunta a direcion de la oficina en concreto';

COMMENT ON COLUMN reserva.oficina_devolucion_propuesta IS  'Análogo a la de recogida.';


-- tarifa
CREATE TABLE IF NOT EXISTS tarifa (
   id_tarifa SERIAL PRIMARY KEY,
   tipo_tarifa tipo_tarifa NOT NULL
);


-- tarifa_cd
CREATE TABLE IF NOT EXISTS tarifa_cd (
   id_tarifa INT NOT NULL,
   tipo_tarifa_cd tipo_tarifa_cd NOT NULL,
   precio DECIMAL(10,2) NOT NULL,
   periodo periodo NOT NULL,
   PRIMARY KEY (id_tarifa, periodo),
   CONSTRAINT fk_tarifa_cd_tarifa1
     FOREIGN KEY (id_tarifa)
     REFERENCES tarifa(id_tarifa)
     ON DELETE NO ACTION
     ON UPDATE NO ACTION
);


-- estado_coche
CREATE TABLE IF NOT EXISTS estado_coche(
   id_coche INT NOT NULL,
   fecha_desde DATE NOT NULL,
   libre BOOLEAN NOT NULL,
   fecha_hasta DATE NULL,
   PRIMARY KEY (id_coche, fecha_desde),
   CONSTRAINT fk_estado_coche_coche1
     FOREIGN KEY (id_coche)
     REFERENCES coche(id)
     ON DELETE NO ACTION
     ON UPDATE NO ACTION
);

CREATE INDEX fk_estado_coche_coche1_idx ON estado_coche (id_coche ASC);


-- tarifa_ld
CREATE TABLE IF NOT EXISTS tarifa_ld(
   id_tarifa SERIAL PRIMARY KEY,
   precio DECIMAL(10,2) NOT NULL,
   CONSTRAINT fk_tarifa_ld_tarifa1
     FOREIGN KEY (id_tarifa)
     REFERENCES tarifa(id_tarifa)
     ON DELETE NO ACTION
     ON UPDATE NO ACTION
);


-- 
CREATE TABLE IF NOT EXISTS documento_pago (
   id_documento SERIAL PRIMARY KEY,
   id_reserva  INT NOT NULL,
   forma_pago  forma_pago NOT NULL,
   importe  DECIMAL(10,2) NOT NULL,
   num_tarjeta  VARCHAR(16) NOT NULL,
   id_oficina  INT NOT NULL,
   CONSTRAINT  fk_documento_pago_reserva1
     FOREIGN KEY (id_reserva)
     REFERENCES reserva(id_reserva)
     ON DELETE NO ACTION
     ON UPDATE NO ACTION,
   CONSTRAINT fk_documento_pago_oficina1
     FOREIGN KEY (id_oficina)
     REFERENCES oficina(id_oficina)
     ON DELETE NO ACTION
     ON UPDATE NO ACTION
);

CREATE INDEX fk_documento_pago_reserva1_idx ON documento_pago (id_reserva ASC);

CREATE INDEX fk_documento_pago_oficina1_idx ON documento_pago (id_oficina ASC);


-- estado_reserva
CREATE TABLE IF NOT EXISTS estado_reserva (
   id_reserva  INT NOT NULL,
   id_estado  estado NOT NULL,
   fecha_desde  DATE NOT NULL,
   PRIMARY KEY (id_reserva, id_estado),
   CONSTRAINT  fk_estado_reserva_reserva1
     FOREIGN KEY (id_reserva)
     REFERENCES reserva(id_reserva)
     ON DELETE NO ACTION
     ON UPDATE NO ACTION
);


CREATE INDEX fk_estado_reserva_reserva1_idx ON estado_reserva (id_reserva ASC);


-- extra
CREATE TABLE IF NOT EXISTS extra(
   id_extra SERIAL PRIMARY KEY,
   descripcion  VARCHAR(45) NOT NULL UNIQUE
);

-- -----------------------------------------------------
-- Table `AutoVeloz`.`historico_precio`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS historico_precio (
   fecha_establecido DATE NOT NULL,
   precio  DECIMAL(10,2) NOT NULL,
   id_extra INT NOT NULL,
   PRIMARY KEY (fecha_establecido, id_extra),
   CONSTRAINT  fk_historico_precio_extra1
     FOREIGN KEY (id_extra)
     REFERENCES extra(id_extra)
     ON DELETE NO ACTION
     ON UPDATE NO ACTION
);

CREATE INDEX fk_historico_precio_extra1_idx ON historico_precio (id_extra ASC);


-- descuento
CREATE TABLE IF NOT EXISTS descuento (
   codigo VARCHAR(10) PRIMARY KEY,
   caducidad  DATE NULL,
   porcentaje  INT NOT NULL,
   id_reserva  INT NULL,
   CONSTRAINT  fk_descuento_reserva1
     FOREIGN KEY (id_reserva)
     REFERENCES reserva(id_reserva)
     ON DELETE NO ACTION
     ON UPDATE NO ACTION
);

CREATE INDEX fk_descuento_reserva1_idx ON descuento (id_reserva ASC);


-- reserva_has_extra
CREATE TABLE IF NOT EXISTS reserva_has_extra (
   id_reserva  INT NOT NULL,
   id_extra  INT NOT NULL,
   PRIMARY KEY (id_reserva, id_extra),
   CONSTRAINT  fk_reserva_has_extra_reserva
     FOREIGN KEY (id_reserva)
     REFERENCES reserva(id_reserva)
     ON DELETE NO ACTION
     ON UPDATE NO ACTION,
   CONSTRAINT fk_reserva_has_extra_extra1
     FOREIGN KEY (id_extra)
     REFERENCES extra(id_extra)
     ON DELETE NO ACTION
     ON UPDATE NO ACTION
);

CREATE INDEX fk_reserva_has_extra_extra1_idx ON reserva_has_extra (id_extra ASC);

CREATE INDEX fk_reserva_has_extra_reserva_idx ON reserva_has_extra (id_reserva ASC);


-- usuario_has_descuento
CREATE TABLE IF NOT EXISTS usuario_has_descuento (
   usuario_id  CHAR(9) NOT NULL,
   descuento_codigo  VARCHAR(10) NOT NULL,
   PRIMARY KEY (usuario_id, descuento_codigo),
   CONSTRAINT  fk_usuario_has_descuento_usuario1
     FOREIGN KEY (usuario_id)
     REFERENCES usuario(id)
     ON DELETE NO ACTION
     ON UPDATE NO ACTION,
   CONSTRAINT fk_usuario_has_descuento_descuento1
     FOREIGN KEY (descuento_codigo)
     REFERENCES descuento(codigo)
     ON DELETE NO ACTION
     ON UPDATE NO ACTION
);

CREATE INDEX fk_usuario_has_descuento_descuento1_idx ON usuario_has_descuento (descuento_codigo ASC);

CREATE INDEX fk_usuario_has_descuento_usuario1_idx ON usuario_has_descuento (usuario_id ASC);


-- coche_en_oficina
CREATE TABLE IF NOT EXISTS coche_en_oficina(
   id_coche  INT NOT NULL,
   id_oficina INT NOT NULL,
   fecha_desde  DATE NOT NULL,
   fecha_hasta  DATE NULL,
   PRIMARY KEY (id_coche, id_oficina, fecha_desde),
   CONSTRAINT  fk_coche_has_oficina_coche1 
     FOREIGN KEY (id_coche)
     REFERENCES coche(id)
     ON DELETE NO ACTION
     ON UPDATE NO ACTION,
   CONSTRAINT fk_coche_has_oficina_oficina1
     FOREIGN KEY (id_oficina)
     REFERENCES oficina(id_oficina)
     ON DELETE NO ACTION
     ON UPDATE NO ACTION
);

CREATE INDEX fk_coche_has_oficina_oficina1_idx ON coche_en_oficina (id_oficina ASC);

CREATE INDEX fk_coche_has_oficina_coche1_idx ON coche_en_oficina (id_coche ASC);


-- documento_has_pago_tarifa
CREATE TABLE IF NOT EXISTS documento_pago_has_tarifa (
   id_documento INT NOT NULL,
   id_tarifa  INT NOT NULL,
   volumen  DOUBLE PRECISION NOT NULL,
   PRIMARY KEY (id_documento, id_tarifa),
   CONSTRAINT fk_documento_pago_has_tarifa_documento_pago1
     FOREIGN KEY (id_documento)
     REFERENCES documento_pago(id_documento)
     ON DELETE NO ACTION
     ON UPDATE NO ACTION,
   CONSTRAINT fk_documento_pago_has_tarifa_tarifa1
     FOREIGN KEY (id_tarifa)
     REFERENCES tarifa(id_tarifa)
     ON DELETE NO ACTION
     ON UPDATE NO ACTION
);

CREATE INDEX fk_documento_pago_has_tarifa_tarifa1_idx ON documento_pago_has_tarifa (id_tarifa ASC);

CREATE INDEX fk_documento_pago_has_tarifa_documento_pago1_idx ON documento_pago_has_tarifa (id_documento ASC);


-- reserva_has_tarifa
CREATE TABLE IF NOT EXISTS reserva_has_tarifa (
   id_reserva INT NOT NULL,
   id_tarifa INT NOT NULL,
   PRIMARY KEY (id_reserva, id_tarifa),
   CONSTRAINT fk_reserva_has_tarifa_reserva1
     FOREIGN KEY (id_reserva)
     REFERENCES reserva(id_reserva)
     ON DELETE NO ACTION
     ON UPDATE NO ACTION,
   CONSTRAINT fk_reserva_has_tarifa_tarifa1
     FOREIGN KEY (id_tarifa)
     REFERENCES tarifa(id_tarifa)
     ON DELETE NO ACTION
     ON UPDATE NO ACTION
);

CREATE INDEX fk_reserva_has_tarifa_tarifa1_idx ON reserva_has_tarifa (id_tarifa ASC);

CREATE INDEX fk_reserva_has_tarifa_reserva1_idx ON reserva_has_tarifa (id_reserva ASC);


-- documento_pago_has_descuento
CREATE TABLE IF NOT EXISTS documento_pago_has_descuento (
   id_documento INT NOT NULL,
   codigo_descuento VARCHAR(10) NOT NULL,
   PRIMARY KEY (id_documento, codigo_descuento),
   CONSTRAINT fk_documento_pago_has_descuento_documento_pago1
     FOREIGN KEY (id_documento)
     REFERENCES documento_pago(id_documento)
     ON DELETE NO ACTION
     ON UPDATE NO ACTION,
   CONSTRAINT fk_documento_pago_has_descuento_descuento1
     FOREIGN KEY (codigo_descuento)
     REFERENCES descuento(codigo)
     ON DELETE NO ACTION
     ON UPDATE NO ACTION
);

CREATE INDEX fk_documento_pago_has_descuento_descuento1_idx ON documento_pago_has_descuento (codigo_descuento ASC);

CREATE INDEX fk_documento_pago_has_descuento_documento_descuento1_idx ON documento_pago_has_descuento (id_documento ASC);


-- documento_pago_has_extra
CREATE TABLE IF NOT EXISTS documento_pago_has_extra (
   id_documento INT NOT NULL,
   id_extra  INT NOT NULL,
   PRIMARY KEY (id_documento, id_extra),
   CONSTRAINT  fk_documento_pago_has_extra_documento_pago1
     FOREIGN KEY (id_documento)
     REFERENCES documento_pago(id_documento)
     ON DELETE NO ACTION
     ON UPDATE NO ACTION,
   CONSTRAINT fk_documento_pago_has_extra_extra1
     FOREIGN KEY (id_extra)
     REFERENCES extra(id_extra)
     ON DELETE NO ACTION
     ON UPDATE NO ACTION
);

CREATE INDEX fk_documento_pago_has_extra_extra1_idx ON documento_pago_has_extra (id_extra ASC);

CREATE INDEX fk_documento_pago_has_extra_documento_pago1_idx ON documento_pago_has_extra (id_documento ASC);


-- modelo_has_tarifa
CREATE TABLE IF NOT EXISTS modelo_has_tarifa (
   modelo VARCHAR(80) NOT NULL,
   categoria categoria NOT NULL,
   id_tarifa  INT NOT NULL,
   PRIMARY KEY (modelo, categoria, id_tarifa),
   CONSTRAINT fk_modelo_has_tarifa_modelo1
     FOREIGN KEY (modelo, categoria)
     REFERENCES modelo(modelo, categoria)
     ON DELETE NO ACTION
     ON UPDATE NO ACTION,
   CONSTRAINT fk_modelo_has_tarifa_tarifa1
     FOREIGN KEY (id_tarifa)
     REFERENCES tarifa(id_tarifa)
     ON DELETE NO ACTION
     ON UPDATE NO ACTION
);


CREATE INDEX fk_modelo_has_tarifa_tarifa1_idx ON modelo_has_tarifa (id_tarifa ASC);

CREATE INDEX fk_modelo_has_tarifa_modelo1_idx ON modelo_has_tarifa (modelo ASC, categoria ASC);


"""

cur.execute(tables_statement)


# to save the changes
conn.commit()

# closes the cursor and conn
cur.close()
conn.close()
