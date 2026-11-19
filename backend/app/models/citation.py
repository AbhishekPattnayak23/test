from datetime import datetime
import uuid
from sqlalchemy import Column, Text, DateTime, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base import Base


class Citation(Base):
    """Citation model linking answers to knowledge sources with relevance scores."""
    
    __tablename__ = "citations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    answer_id = Column(UUID(as_uuid=True), ForeignKey("answers.id"), nullable=False)
    knowledge_source_id = Column(UUID(as_uuid=True), ForeignKey("knowledge_sources.id"), nullable=False)
    snippet_text = Column(Text, nullable=False)
    relevance_score = Column(Float, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    answer = relationship("Answer", back_populates="citations")
    knowledge_source = relationship("KnowledgeSource", back_populates="citations")
    
    def __repr__(self) -> str:
        return f"<Citation(id={self.id}, relevance={self.relevance_score})>"
    
    def to_dict(self) -> dict:
        """Convert citation to dictionary."""
        return {
            "id": str(self.id),
            "answer_id": str(self.answer_id),
            "knowledge_source_id": str(self.knowledge_source_id),
            "snippet_text": self.snippet_text,
            "relevance_score": self.relevance_score,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
