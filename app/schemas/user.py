"""
Scheme Pydantic pentru validarea și serializarea datelor User
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, validator
import re

class UserBase(BaseModel):
    """Schema de bază pentru User - câmpuri comune"""
    full_name: str = Field(..., min_length=2, max_length=100, description="Numele complet")
    email: EmailStr = Field(..., description="Adresa de email validă")
    phone: str = Field(..., description="Numărul de telefon în format românesc")
    username: str = Field(..., min_length=3, max_length=30, description="Numele de utilizator")
    age: int = Field(..., ge=13, le=120, description="Vârsta între 13 și 120 ani")

    @validator('phone')
    def validate_phone(cls, v):
        """Validare format telefon românesc (07xxxxxxxx)"""
        if not re.match(r'^07[0-9]{8}$', v):
            raise ValueError('Numărul de telefon trebuie să fie în format românesc (07xxxxxxxx)')
        return v

    @validator('username')
    def validate_username(cls, v):
        """Validare username - doar alfanumeric"""
        if not re.match(r'^[a-zA-Z0-9]+$', v):
            raise ValueError('Username-ul poate conține doar caractere alfanumerice')
        return v

    @validator('full_name')
    def validate_full_name(cls, v):
        """Validare nume complet - minim 2 cuvinte"""
        if len(v.strip().split()) < 2:
            raise ValueError('Numele complet trebuie să conțină prenumele și numele')
        return v.strip()

class UserCreate(UserBase):
    """Schema pentru crearea unui utilizator nou"""
    password: str = Field(..., min_length=6, max_length=100, description="Parola cu minim 6 caractere")
    confirmPassword: str = Field(..., description="Confirmarea parolei")

    @validator('confirmPassword')
    def passwords_match(cls, v, values):
        """Validare că parolele se potrivesc"""
        if 'password' in values and v != values['password']:
            raise ValueError('Parolele nu se potrivesc')
        return v

class UserLogin(BaseModel):
    """Schema pentru autentificare"""
    identifier: str = Field(..., description="Email, username sau telefon")
    password: str = Field(..., description="Parola")

class UserResponse(UserBase):
    """Schema pentru răspunsul cu datele utilizatorului (fără parolă)"""
    id: int
    is_first_login: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        """Configurare pentru serializarea din SQLAlchemy ORM"""
        from_attributes = True

class UserUpdate(BaseModel):
    """Schema pentru actualizarea profilului"""
    full_name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    age: Optional[int] = Field(None, ge=13, le=120)

    @validator('phone')
    def validate_phone(cls, v):
        """Validare format telefon românesc (07xxxxxxxx)"""
        if v and not re.match(r'^07[0-9]{8}$', v):
            raise ValueError('Numărul de telefon trebuie să fie în format românesc (07xxxxxxxx)')
        return v

class Token(BaseModel):
    """Schema pentru token-ul JWT"""
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    """Schema pentru datele din token"""
    username: Optional[str] = None 