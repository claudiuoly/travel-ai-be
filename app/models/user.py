"""
Model User pentru baza de date
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    """
    Model pentru tabelul users
    Conține toate informațiile necesare pentru autentificare și profilul utilizatorului
    """
    __tablename__ = "users"

    # Primary key - ID unic auto-incrementat
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Informații personale
    full_name = Column(String, nullable=False, comment="Numele complet al utilizatorului")
    email = Column(String, unique=True, nullable=False, index=True, comment="Adresa de email unică")
    phone = Column(String, unique=True, nullable=False, index=True, comment="Numărul de telefon unic")
    username = Column(String, unique=True, nullable=False, index=True, comment="Numele de utilizator unic")
    age = Column(Integer, nullable=False, comment="Vârsta utilizatorului")
    
    # Securitate
    password = Column(String, nullable=False, comment="Parola hash-uită cu bcrypt")
    is_first_login = Column(Boolean, default=True, nullable=False, comment="Flag pentru primul login")
    
    # Timestamps - gestionate automat
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, comment="Data și ora creării")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False, comment="Data și ora ultimei actualizări")

    # Relație cu mesajele de chat
    messages = relationship("ChatMessage", back_populates="user")

    def __repr__(self):
        """Reprezentare string pentru debugging"""
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>" 