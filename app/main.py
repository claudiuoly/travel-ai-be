"""
Aplicația principală FastAPI pentru Travel AI Backend
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import uvicorn

# Import-uri locale
from app.database import create_tables, engine
from app.routers import auth, chat
from app.config import HOST, PORT, DEBUG

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Context manager pentru gestionarea ciclului de viață al aplicației
    Se execută la pornire și oprire
    """
    # Operațiuni la pornire
    print("🚀 Pornesc aplicația Travel AI Backend...")
    
    # Creează tabelele în baza de date
    try:
        create_tables()
        print("✅ Tabelele au fost create cu succes!")
    except Exception as e:
        print(f"❌ Eroare la crearea tabelelor: {e}")
    
    print("🎯 Serverul este gata să primească cereri!")
    yield
    
    # Operațiuni la oprire
    print("🛑 Opresc aplicația...")
    engine.dispose()
    print("✅ Baza de date închisă cu succes!")

# Crearea aplicației FastAPI
app = FastAPI(
    title="Travel AI Backend",
    description="Backend pentru aplicația Travel AI - sistem de autentificare și gestionare utilizatori",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configurare CORS pentru frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite toate originile pentru dezvoltare
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Includerea router-urilor
app.include_router(auth.router)
app.include_router(chat.router)

# Handler global pentru excepții
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Handler global pentru toate excepțiile neprévăzute
    """
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

# Rută de test pentru verificarea stării serverului
@app.get("/", tags=["Health Check"])
async def root():
    """
    Rută de verificare a stării serverului
    """
    return {
        "message": "Travel AI Backend este funcțional!",
        "version": "1.0.0",
        "status": "active",
        "docs": "/docs"
    }

@app.get("/health", tags=["Health Check"])
async def health_check():
    """
    Verificare detaliată a stării sistemului
    """
    try:
        # Testează conexiunea la baza de date
        from app.database import SessionLocal
        from sqlalchemy import text
        from datetime import datetime
        
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        db_status = "connected"
    except Exception:
        db_status = "disconnected"
    
    return {
        "status": "healthy" if db_status == "connected" else "unhealthy",
        "database": db_status,
        "timestamp": datetime.now().isoformat()
    }

# Punct de intrare pentru rularea aplicației
if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=HOST,
        port=PORT,
        reload=DEBUG,
        log_level="info"
    ) 