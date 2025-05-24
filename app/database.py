"""
Configurare bază de date PostgreSQL cu SQLAlchemy
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import DATABASE_URL

# Crearea engine-ului pentru baza de date
engine = create_engine(DATABASE_URL)

# Crearea session maker-ului pentru gestionarea sesiunilor de bază de date
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clasa de bază pentru toate modelele
Base = declarative_base()

def get_db():
    """
    Dependency pentru obținerea unei sesiuni de bază de date
    Asigură închiderea automată a sesiunii după utilizare
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """
    Creează toate tabelele în baza de date
    Apelat la pornirea aplicației
    """
    Base.metadata.create_all(bind=engine) 