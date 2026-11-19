"""
Villa model for CV Villas Agent Assist.

Defines the Villa entity representing vacation properties.
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base import Base


class Villa(Base):
    """Villa model representing vacation properties."""

    __tablename__ = "villas"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    location = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    amenities_json = Column(JSON, nullable=True)  # Stores amenities as JSON { "pool": true, "wifi": true, ... }
    price_range = Column(String(100), nullable=True)  # e.g., "$1000-$2000 per week"
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    agent_plans = relationship("AgentPlan", back_populates="villa", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Villa(id={self.id}, name='{self.name}', location='{self.location}')>"

    def to_dict(self) -> dict:
        """Convert villa to dictionary."""
        return {
            "id": str(self.id),
            "name": self.name,
            "location": self.location,
            "description": self.description,
            "amenities": self.amenities_json if self.amenities_json else {},
            "price_range": self.price_range,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }