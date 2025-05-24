#!/usr/bin/env python3
"""
Script pentru pornirea serverului Travel AI Backend
Utilizare: python3 start_server.py
"""
import uvicorn
from app.config import HOST, PORT, DEBUG

if __name__ == "__main__":
    print("🚀 Pornesc Travel AI Backend...")
    print(f"📍 Server: http://{HOST}:{PORT}")
    print(f"📖 API Docs: http://{HOST}:{PORT}/docs")
    print(f"🔧 Debug Mode: {DEBUG}")
    print("-" * 50)
    
    uvicorn.run(
        "app.main:app",
        host=HOST,
        port=PORT,
        reload=DEBUG,
        log_level="info"
    ) 