"""
Model pentru mesajele de chat
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class ChatMessage(Base):
    """
    Model pentru tabelul chat_messages
    Stochează mesajele utilizatorilor și răspunsurile chatbot-ului
    """
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message = Column(String, nullable=False)
    is_user = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relație cu utilizatorul
    user = relationship("User", back_populates="messages")

    def __repr__(self):
        return f"<ChatMessage(id={self.id}, user_id={self.user_id}, is_user={self.is_user})>" 