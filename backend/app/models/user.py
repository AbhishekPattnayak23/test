"""
User model for CV Villas Agent Assist.

Defines the User entity with roles: guest, agent, expert, admin.
"""
import uuid
from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy import Column, String, DateTime, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base import Base


class UserRole(PyEnum):
    """User role enumeration."""
    GUEST = "guest"
    AGENT = "agent"
    EXPERT = "expert"
    ADMIN = "admin"


class User(Base):
    """User model representing system users."""
    
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(SQLEnum(UserRole), nullable=False, default=UserRole.GUEST)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    answers = relationship("Answer", back_populates="user", cascade="all, delete-orphan")
    expert_corrections = relationship("ExpertCorrection", back_populates="corrected_by_user", foreign_keys="ExpertCorrection.corrected_by_user_id")
    coverage_gaps = relationship("CoverageGap", back_populates="assigned_to_user", foreign_keys="CoverageGap.assigned_to_user_id")
    escalated_by = relationship("Escalation", back_populates="escalated_by_user", foreign_keys="Escalation.escalated_by_user_id")
    assigned_escalations = relationship("Escalation", back_populates="assigned_to_user", foreign_keys="Escalation.assigned_to_user_id")
    audit_logs = relationship("AuditLog", back_populates="user")
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email}, role={self.role.value})>"
    
    def to_dict(self) -> dict:
        """Convert user to dictionary."""
        return {
            "id": str(self.id),
            "email": self.email,
            "role": self.role.value,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }