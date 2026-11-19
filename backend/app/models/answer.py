from datetime import datetime
import uuid
from sqlalchemy import Column, String, Text, DateTime, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base import Base


class Answer(Base):
    """Answer model representing generated answers to questions."""
    
    __tablename__ = "answers"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    question_text = Column(Text, nullable=False)
    answer_text = Column(Text, nullable=False)
    confidence_score = Column(Float, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="answers")
    citations = relationship("Citation", back_populates="answer", cascade="all, delete-orphan")
    expert_corrections = relationship("ExpertCorrection", back_populates="answer", cascade="all, delete-orphan")
    escalations = relationship("Escalation", back_populates="answer", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<Answer(id={self.id}, confidence={self.confidence_score})>"
    
    def to_dict(self) -> dict:
        """Convert answer to dictionary."""
        return {
            "id": str(self.id),
            "question_text": self.question_text,
            "answer_text": self.answer_text,
            "confidence_score": self.confidence_score,
            "user_id": str(self.user_id),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
