# 🚀 Backend - Proyecto Autoveloz

Este repositorio contiene el backend del proyecto **Autoveloz**.

---

## 🍏 Entorno de desarrollo en macOS

### 1. Crear y activar entorno virtual (si no existe):

```bash
python3.11 -m venv venvmac
source venvmac/bin/activate
```

### 2. Instalar dependencias del sistema:

`psycopg2` depende de `libpq`, que requiere instalación manual en macOS.

```bash
brew install libpq
brew link --force libpq
```

### 3. Instalar paquetes Python:

```bash
pip install -r requirements.txt
```

---

## 🌐 Instalar PostgreSQL

Descargar e instalar desde: 👉 [https://www.postgresql.org/](https://www.postgresql.org/)

---

## 🔧 Configurar la base de datos

Una vez instalado PostgreSQL, crea la base de datos y el usuario con privilegios:

```sql
CREATE USER autoveloz_creator WITH ENCRYPTED PASSWORD 'autovelozGPI';
ALTER DATABASE autoveloz OWNER TO autoveloz_creator;
GRANT ALL PRIVILEGES ON SCHEMA public TO autoveloz_creator;
```

---

## 📂 Poblar la base de datos de pruebas

Ejecuta el script para rellenar la base de datos local:

```bash
python db.py
```

---

## 🚀 Lanzar la aplicación

```bash
uvicorn main:app --reload
```

Esto levantará el servidor de desarrollo en modo recarga automática.

---

## 🔍 Probar las APIs

Accede a la documentación interactiva de la API con Swagger:

🔗 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)


