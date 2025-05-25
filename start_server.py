#!/usr/bin/env python3
"""
Script pentru pornirea serverului Travel AI Backend
Utilizare: python3 start_server.py
"""
import uvicorn
import logging
from app.config import HOST, PORT, DEBUG

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    try:
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
            log_level="debug",
            workers=1
        )
    except Exception as e:
        logger.error(f"Error starting server: {str(e)}")
        raise 