"""
Scheme pentru mesajele de chat
"""
from pydantic import BaseModel, Field
from datetime import datetime

class ChatRequest(BaseModel):
    """Schema pentru cererea de chat"""
    message: str = Field(..., min_length=1, max_length=1000, description="Mesajul utilizatorului")

class ChatResponse(BaseModel):
    """Schema pentru răspunsul chatbot-ului"""
    message: str = Field(..., description="Răspunsul chatbot-ului")
    user_id: int = Field(..., description="ID-ul utilizatorului")
    created_at: datetime = Field(default_factory=datetime.now, description="Data și ora răspunsului") 