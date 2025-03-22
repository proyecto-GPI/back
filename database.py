#database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# url with the user, pass and name of the database
url="postgresql://autoveloz_creator:autovelozGPI@localhost:5432/autoveloz"


engine = create_engine(url)



SessionLocal = sessionmaker( autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
