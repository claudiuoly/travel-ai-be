#!/usr/bin/env python3
"""
Script curat pentru pornirea serverului Travel AI Backend
Fără warning-uri Chromium/Electron și fără auto-reload
"""
import os
import uvicorn
from app.config import HOST, PORT, DEBUG

# Dezactivează variabilele de mediu GUI pentru a evita warning-urile Chromium/Electron
os.environ.pop('DISPLAY', None)
os.environ.pop('WAYLAND_DISPLAY', None)
os.environ.pop('XDG_SESSION_TYPE', None)
os.environ.pop('CHROME_DESKTOP', None)

# Dezactivează editorul pentru a preveni deschiderea automată a Cursor
os.environ.pop('EDITOR', None)
os.environ.pop('VISUAL', None)
os.environ['EDITOR'] = 'true'  # Setează un editor dummy

if __name__ == "__main__":
    print("🚀 Pornesc Travel AI Backend (Clean Mode)...")
    print(f"📍 Server: http://{HOST}:{PORT}")
    print(f"📖 API Docs: http://{HOST}:{PORT}/docs")
    print(f"🔧 Debug Mode: {DEBUG}")
    print("✅ GUI warnings disabled")
    print("✅ Auto-reload disabled pentru stabilitate")
    print("-" * 50)
    
    uvicorn.run(
        "app.main:app",
        host=HOST,
        port=PORT,
        reload=False,  # Dezactivează auto-reload
        log_level="info"
    ) 