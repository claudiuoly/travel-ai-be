"""
Utilitare pentru autentificare JWT și gestionarea token-urilor
"""
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_HOURS
from app.database import get_db
from app.models.user import User
from app.schemas.user import TokenData

# Security scheme pentru Bearer token
security = HTTPBearer()

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Creează un token JWT cu datele și timpul de expirare specificat
    
    Args:
        data (dict): Datele de inclus în token
        expires_delta (timedelta, optional): Timpul de expirare. Default: 24 ore
        
    Returns:
        str: Token-ul JWT generat
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt

def verify_token(token: str, credentials_exception: HTTPException) -> TokenData:
    """
    Verifică și decodează un token JWT
    
    Args:
        token (str): Token-ul JWT de verificat
        credentials_exception (HTTPException): Excepția de aruncat în caz de eroare
        
    Returns:
        TokenData: Datele din token
        
    Raises:
        HTTPException: Dacă token-ul este invalid
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        
        if username is None:
            raise credentials_exception
            
        token_data = TokenData(username=username)
        return token_data
        
    except JWTError:
        raise credentials_exception

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)) -> User:
    """
    Obține utilizatorul curent pe baza token-ului JWT
    
    Args:
        credentials: Credențialele Bearer din header
        db: Sesiunea de bază de date
        
    Returns:
        User: Utilizatorul curent autentificat
        
    Raises:
        HTTPException: Dacă token-ul este invalid sau utilizatorul nu există
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Verifică token-ul și extrage datele
    token_data = verify_token(credentials.credentials, credentials_exception)
    
    # Caută utilizatorul în baza de date
    user = db.query(User).filter(User.username == token_data.username).first()
    
    if user is None:
        raise credentials_exception
        
    return user 