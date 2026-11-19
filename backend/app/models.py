"""
SQLAlchemy ORM models for CV Villas Knowledge Assistant.
Authoritative models based on system requirements.
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import (
    Column, Integer, String, Float, Boolean, Text, DateTime,
    ForeignKey, JSON, Index, Table, UniqueConstraint,
    create_engine
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, Session
from sqlalchemy.sql import func

Base = declarative_base()


class User(Base):
    """User accounts with role-based access control."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), index=True)
    full_name = Column(String(255))
    role = Column(String(50), nullable=False, default="agent")  # guest, agent, expert, admin
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    answers = relationship("Answer", back_populates="user")
    expert_corrections = relationship("ExpertCorrection", back_populates="expert_user", foreign_keys="ExpertCorrection.corrected_by_user_id")
    audit_logs = relationship("AuditLog", back_populates="user")
    agent_plans = relationship("AgentPlan", back_populates="agent")
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"


class Villa(Base):
    """Villa properties available for rental."""
    __tablename__ = "villas"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    location = Column(String(255), nullable=False, index=True)
    country = Column(String(100))
    region = Column(String(100))
    description = Column(Text)
    amenities = Column(JSON, default=list)  # List of amenities
    price_range_min = Column(Integer)  # Per week
    price_range_max = Column(Integer)  # Per week
    bedrooms = Column(Integer)
    bathrooms = Column(Integer)
    capacity = Column(Integer)
    images = Column(JSON, default=list)  # List of image URLs
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    knowledge_sources = relationship("KnowledgeSource", back_populates="villa", foreign_keys="KnowledgeSource.villa_id")
    
    def __repr__(self):
        return f"<Villa(id={self.id}, name={self.name}, location={self.location})>"


class KnowledgeSource(Base):
    """Knowledge content used for RAG pipeline."""
    __tablename__ = "knowledge_sources"
    
    id = Column(Integer, primary_key=True, index=True)
    villa_id = Column(Integer, ForeignKey("villas.id"), index=True, nullable=True)
    type = Column(String(50), nullable=False, index=True)  # faq, policy, amenity_detail, region_guide, etc.
    title = Column(String(500), nullable=False)
    content = Column(Text, nullable=False)
    embedding_vector = Column(JSON)  # Stored as JSON array for now
    metadata = Column(JSON, default=dict)
    source_uri = Column(String(500))
    version = Column(Integer, default=1)
    is_active = Column(Boolean, default=True)
    ingested_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    villa = relationship("Villa", back_populates="knowledge_sources")
    citations = relationship("Citation", back_populates="knowledge_source")
    
    def __repr__(self):
        return f"<KnowledgeSource(id={self.id}, type={self.type}, title={self.title[:50]}...)>"


class Answer(Base):
    """Generated answers to user questions."""
    __tablename__ = "answers"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    question = Column(Text, nullable=False)
    answer_text = Column(Text, nullable=False)
    confidence_score = Column(Float, default=0.0, index=True)
    source_type = Column(String(50))  # rag, template, expert_correction, etc.
    is_escalated = Column(Boolean, default=False)
    escalation_reason = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="answers")
    citations = relationship("Citation", back_populates="answer")
    expert_corrections = relationship("ExpertCorrection", back_populates="answer")
    coverage_gaps = relationship("CoverageGap", back_populates="answer")
    escalations = relationship("Escalation", back_populates="answer")
    
    def __repr__(self):
        return f"<Answer(id={self.id}, confidence={self.confidence_score})>"


class Citation(Base):
    """Citations linking answers to knowledge sources."""
    __tablename__ = "citations"
    
    id = Column(Integer, primary_key=True, index=True)
    answer_id = Column(Integer, ForeignKey("answers.id"), index=True, nullable=False)
    source_id = Column(Integer, ForeignKey("knowledge_sources.id"), index=True, nullable=False)
    excerpt = Column(Text)
    relevance_score = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    answer = relationship("Answer", back_populates="citations")
    knowledge_source = relationship("KnowledgeSource", back_populates="citations")
    
    def __repr__(self):
        return f"<Citation(id={self.id}, answer={self.answer_id}, source={self.source_id})>"


class ExpertCorrection(Base):
    """Expert corrections submitted for answers."""
    __tablename__ = "expert_corrections"
    
    id = Column(Integer, primary_key=True, index=True)
    answer_id = Column(Integer, ForeignKey("answers.id"), index=True, nullable=False)
    corrected_by_user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    correction_text = Column(Text, nullable=False)
    original_text = Column(Text)  # Store original answer text for comparison
    reason = Column(Text)
    status = Column(String(50), default="pending", index=True)  # pending, approved, rejected
    reviewed_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    review_notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    answer = relationship("Answer", back_populates="expert_corrections")
    expert_user = relationship("User", back_populates="expert_corrections", foreign_keys=[corrected_by_user_id])
    reviewer = relationship("User", foreign_keys=[reviewed_by_user_id])
    
    def __repr__(self):
        return f"<ExpertCorrection(id={self.id}, status={self.status})>"


class AuditLog(Base):
    """Audit trail for all system actions."""
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=True)
    action = Column(String(100), nullable=False, index=True)  # create, update, delete, login, etc.
    entity_type = Column(String(100), index=True)  # user, villa, answer, etc.
    entity_id = Column(Integer, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    metadata = Column(JSON, default=dict)
    ip_address = Column(String(50))
    user_agent = Column(String(500))
    
    # Relationships
    user = relationship("User", back_populates="audit_logs")
    
    def __repr__(self):
        return f"<AuditLog(id={self.id}, action={self.action}, entity={self.entity_type})>"


class CoverageGap(Base):
    """Identified gaps in knowledge coverage."""
    __tablename__ = "coverage_gaps"
    
    id = Column(Integer, primary_key=True, index=True)
    answer_id = Column(Integer, ForeignKey("answers.id"), index=True, nullable=False)
    question = Column(Text, nullable=False)
    confidence_score = Column(Float)
    gap_type = Column(String(100))  # missing_source, outdated_info, ambiguous, etc.
    priority = Column(String(50), default="medium")  # low, medium, high, critical
    status = Column(String(50), default="open", index=True)  # open, investigating, resolved
    assigned_to_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    resolution_notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    answer = relationship("Answer", back_populates="coverage_gaps")
    assigned_to = relationship("User", foreign_keys=[assigned_to_user_id])
    
    def __repr__(self):
        return f"<CoverageGap(id={self.id}, gap_type={self.gap_type}, priority={self.priority})>"


class Escalation(Base):
    """Escalation workflow for low-confidence answers."""
    __tablename__ = "escalations"
    
    id = Column(Integer, primary_key=True, index=True)
    answer_id = Column(Integer, ForeignKey("answers.id"), index=True, nullable=False)
    escalated_by_user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    escalated_to_user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=True)
    reason = Column(Text)
    status = Column(String(50), default="open", index=True)  # open, assigned, in_progress, resolved
    resolution = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    resolved_at = Column(DateTime(timezone=True))
    
    # Relationships
    answer = relationship("Answer", back_populates="escalations")
    escalated_by = relationship("User", foreign_keys=[escalated_by_user_id])
    escalated_to = relationship("User", foreign_keys=[escalated_to_user_id])
    
    def __repr__(self):
        return f"<Escalation(id={self.id}, status={self.status})>"


class AgentPlan(Base):
    """Agent-specific plans and preferences."""
    __tablename__ = "agent_plans"
    
    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    plan_name = Column(String(255), nullable=False)
    preferences = Column(JSON, default=dict)
    targets = Column(JSON, default=dict)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    agent = relationship("User", back_populates="agent_plans")
    
    def __repr__(self):
        return f"<AgentPlan(id={self.id}, agent={self.agent_id}, name={self.plan_name})>"


class Configuration(Base):
    """System configuration settings."""
    __tablename__ = "configuration"
    
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(255), unique=True, index=True, nullable=False)
    value = Column(JSON, nullable=False)
    value_type = Column(String(50), default="string")  # string, integer, float, boolean, json
    category = Column(String(100), index=True)
    description = Column(Text)
    is_encrypted = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<Configuration(id={self.id}, key={self.key})>"


# Create indexes for performance
Index("idx_answers_created_at", Answer.created_at.desc())
Index("idx_knowledge_sources_type_active", KnowledgeSource.type, KnowledgeSource.is_active)
Index("idx_expert_corrections_status_created", ExpertCorrection.status, ExpertCorrection.created_at.desc())
Index("idx_audit_logs_timestamp", AuditLog.timestamp.desc())
Index("idx_users_role_active", User.role, User.is_active)