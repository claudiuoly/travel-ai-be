"""
Router pentru autentificare - login și register
"""
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import logging
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.utils.password import hash_password, verify_password
from app.utils.auth import create_access_token
from app.config import ACCESS_TOKEN_EXPIRE_HOURS

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Crearea router-ului pentru autentificare
router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/register", response_model=dict, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Înregistrează un utilizator nou în sistem
    
    Args:
        user_data (UserCreate): Datele utilizatorului pentru înregistrare
        db (Session): Sesiunea de bază de date
        
    Returns:
        dict: Mesaj de succes, datele utilizatorului și token-ul JWT
        
    Raises:
        HTTPException: Dacă email/username/telefon există deja
    """
    try:
        logger.debug(f"Attempting to register user with email: {user_data.email}")
        
        # Verifică dacă utilizatorul există deja
        existing_user = db.query(User).filter(
            (User.email == user_data.email) |
            (User.username == user_data.username) |
            (User.phone == user_data.phone)
        ).first()
        
        if existing_user:
            if existing_user.email == user_data.email:
                logger.warning(f"Email already registered: {user_data.email}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email-ul este deja înregistrat"
                )
            elif existing_user.username == user_data.username:
                logger.warning(f"Username already taken: {user_data.username}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username-ul este deja utilizat"
                )
            elif existing_user.phone == user_data.phone:
                logger.warning(f"Phone already registered: {user_data.phone}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Numărul de telefon este deja înregistrat"
                )
        
        logger.debug("Creating new user...")
        # Creează utilizatorul nou
        hashed_password = hash_password(user_data.password)
        db_user = User(
            full_name=user_data.full_name,
            email=user_data.email,
            phone=user_data.phone,
            username=user_data.username,
            age=user_data.age,
            password=hashed_password,
            is_first_login=True
        )
        
        logger.debug("Adding user to database...")
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        logger.debug(f"User created successfully with ID: {db_user.id}")
        
        # Creează token-ul JWT
        access_token_expires = timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
        access_token = create_access_token(
            data={"sub": db_user.username},
            expires_delta=access_token_expires
        )
        
        # Pregătește răspunsul
        user_response = UserResponse.from_orm(db_user)
        
        return {
            "message": "User registered successfully",
            "user": user_response.dict(),
            "token": access_token
        }
        
    except IntegrityError as e:
        logger.error(f"Database integrity error: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Datele introduse nu sunt unice. Verificați email-ul, username-ul și telefonul."
        )
    except Exception as e:
        logger.error(f"Unexpected error during registration: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Eroare internă la înregistrare: {str(e)}"
        )

@router.post("/login", response_model=dict)
async def login_user(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Autentifică un utilizator în sistem
    
    Args:
        credentials (UserLogin): Credențialele pentru autentificare (identifier + password)
        db (Session): Sesiunea de bază de date
        
    Returns:
        dict: Mesaj de succes, datele utilizatorului și token-ul JWT
        
    Raises:
        HTTPException: Dacă credențialele sunt incorecte
    """
    try:
        # Caută utilizatorul după email, username sau telefon
        user = db.query(User).filter(
            (User.email == credentials.identifier) |
            (User.username == credentials.identifier) |
            (User.phone == credentials.identifier)
        ).first()
        
        # Verifică dacă utilizatorul există
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credențiale incorecte"
            )
        
        # Verifică parola
        if not verify_password(credentials.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credențiale incorecte"
            )
        
        # Actualizează is_first_login la False după primul login reușit
        if user.is_first_login:
            user.is_first_login = False
            db.commit()
            db.refresh(user)
        
        # Creează token-ul JWT
        access_token_expires = timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
        access_token = create_access_token(
            data={"sub": user.username},
            expires_delta=access_token_expires
        )
        
        # Pregătește răspunsul
        user_response = UserResponse.from_orm(user)
        
        return {
            "message": "Login successful",
            "user": user_response.dict(),
            "token": access_token
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Eroare internă la autentificare"
        ) 