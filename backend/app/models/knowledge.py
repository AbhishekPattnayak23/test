from datetime import datetime
import uuid
from enum import Enum as PyEnum
from sqlalchemy import Column, String, Text, DateTime, Enum as SQLEnum, LargeBinary
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base import Base


class SourceType(PyEnum):
    """Knowledge source type enumeration."""
    KNOWLEDGE_BASE = "knowledge_base"
    CRM_NOTES = "crm_notes"
    WEBSITE = "website"
    DOCUMENTATION = "documentation"


class KnowledgeSource(Base):
    """Knowledge source model representing institutional knowledge."""
    
    __tablename__ = "knowledge_sources"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_type = Column(SQLEnum(SourceType), nullable=False)
    source_url = Column(String(500), nullable=True)
    content_text = Column(Text, nullable=False)
    embedding_vector = Column(LargeBinary, nullable=True)  # Store embeddings as bytes
    indexed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    citations = relationship("Citation", back_populates="knowledge_source", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<KnowledgeSource(id={self.id}, type={self.source_type.value})>"
    
    def to_dict(self) -> dict:
        """Convert knowledge source to dictionary."""
        return {
            "id": str(self.id),
            "source_type": self.source_type.value,
            "source_url": self.source_url,
            "content_text": self.content_text,
            "indexed_at": self.indexed_at.isoformat() if self.indexed_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
