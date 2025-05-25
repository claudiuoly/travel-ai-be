"""
Router pentru funcționalitatea de chat
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.chat import ChatMessage
from app.schemas.chat import ChatRequest, ChatResponse
from app.utils.chat import get_gemini_response
from app.utils.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/chat", tags=["Chat"])

@router.post("/message")
async def send_message(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Trimite un mesaj către chatbot și primește răspunsul
    
    Args:
        request (ChatRequest): Mesajul utilizatorului
        db (Session): Sesiunea de bază de date
        current_user (User): Utilizatorul autentificat
        
    Returns:
        ChatResponse: Răspunsul chatbot-ului
    """
    try:
        # Salvează mesajul utilizatorului
        user_message = ChatMessage(
            user_id=current_user.id,
            message=request.message,
            is_user=True
        )
        db.add(user_message)
        db.commit()
        
        # Obține răspunsul de la Gemini
        response = await get_gemini_response(request.message)
        
        # Salvează răspunsul chatbot-ului
        bot_message = ChatMessage(
            user_id=current_user.id,
            message=response,
            is_user=False
        )
        db.add(bot_message)
        db.commit()
        
        return {"message": response}
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Eroare la procesarea mesajului: {str(e)}"
        ) 