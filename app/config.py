"""
Configurare aplicație - gestionează variabilele de mediu și setările globale
"""
import os
from dotenv import load_dotenv

# Încărcare variabile de mediu din .env
load_dotenv()

# Configurare bază de date
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/travel_ai_db")

# Configurare JWT
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here-change-in-production")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_HOURS = int(os.getenv("ACCESS_TOKEN_EXPIRE_HOURS", "24"))

# Configurare server
HOST = os.getenv("HOST", "localhost")
PORT = int(os.getenv("PORT", "8000"))
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

# Configurare Gemini AI
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyAJ9fgKcsQRhkBYfbok5zcwipGD0xhMT00") 