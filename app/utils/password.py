"""
Utilitare pentru gestionarea parolelor - hash și verificare cu bcrypt
"""
from passlib.context import CryptContext

# Context pentru hash-uirea parolelor cu bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """
    Hash-uiește o parolă folosind bcrypt
    
    Args:
        password (str): Parola în text clar
        
    Returns:
        str: Parola hash-uită
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifică dacă o parolă în text clar se potrivește cu hash-ul
    
    Args:
        plain_password (str): Parola în text clar
        hashed_password (str): Parola hash-uită din baza de date
        
    Returns:
        bool: True dacă parolele se potrivesc, False altfel
    """
    return pwd_context.verify(plain_password, hashed_password) 