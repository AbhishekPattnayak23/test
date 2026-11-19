#!/usr/bin/env python3
"""
Database seeding script for CV Villas Agent Assist.
Creates synthetic data for development and testing.
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path so we can import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models import (
    User, Villa, KnowledgeSource, Answer, Citation, 
    ExpertCorrection, AuditLog, CoverageGap, Escalation,
    AgentPlan, Configuration
)
from datetime import datetime, timedelta
import bcrypt
import json


def create_users(session: Session):
    """Create synthetic users with different roles."""
    password = "password123".encode('utf-8')
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')
    
    users = [
        User(
            id=1,
            email="admin@cvvillas.com",
            hashed_password=hashed_password,
            full_name="Admin User",
            role="admin",
            is_active=True,
            created_at=datetime.utcnow() - timedelta(days=30),
            last_login_at=datetime.utcnow() - timedelta(hours=2)
        ),
        User(
            id=2,
            email="expert@cvvillas.com",
            hashed_password=hashed_password,
            full_name="Expert Reviewer",
            role="expert",
            is_active=True,
            created_at=datetime.utcnow() - timedelta(days=25),
            last_login_at=datetime.utcnow() - timedelta(hours=5)
        ),
        User(
            id=3,
            email="agent1@cvvillas.com",
            hashed_password=hashed_password,
            full_name="Sales Agent 1",
            role="agent",
            is_active=True,
            created_at=datetime.utcnow() - timedelta(days=20),
            last_login_at=datetime.utcnow() - timedelta(hours=12)
        ),
        User(
            id=4,
            email="agent2@cvvillas.com",
            hashed_password=hashed_password,
            full_name="Sales Agent 2",
            role="agent",
            is_active=True,
            created_at=datetime.utcnow() - timedelta(days=15),
            last_login_at=datetime.utcnow() - timedelta(days=1)
        ),
        User(
            id=5,
            email="guest@cvvillas.com",
            hashed_password=hashed_password,
            full_name="Guest User",
            role="guest",
            is_active=True,
            created_at=datetime.utcnow() - timedelta(days=10),
            last_login_at=datetime.utcnow() - timedelta(days=2)
        ),
    ]
    
    session.add_all(users)
    session.commit()
    print(f"Created {len(users)} users")
    return users


def create_villas(session: Session):
    """Create synthetic villa data."""
    villas = [
        Villa(
            id=1,
            name="Seaside Villa",
            location="Malibu, California",
            description="Luxury beachfront villa with panoramic ocean views",
            amenities=json.dumps(["pool", "jacuzzi", "beach access", "wifi", "air conditioning", "gourmet kitchen"]),
            price_range=json.dumps({"min": 5000, "max": 8000}),
            bedroom_count=5,
            bathroom_count=4,
            max_guests=10,
            is_active=True,
            created_at=datetime.utcnow() - timedelta(days=28)
        ),
        Villa(
            id=2,
            name="Mountain Retreat",
            location="Aspen, Colorado",
            description="Ski-in/ski-out chalet with cozy fireplace",
            amenities=json.dumps(["fireplace", "hot tub", "sauna", "wifi", "parking", "game room"]),
            price_range=json.dumps({"min": 4000, "max": 6500}),
            bedroom_count=4,
            bathroom_count=3,
            max_guests=8,
            is_active=True,
            created_at=datetime.utcnow() - timedelta(days=25)
        ),
        Villa(
            id=3,
            name="Urban Penthouse",
            location="New York, NY",
            description="Modern penthouse with city skyline views",
            amenities=json.dumps(["rooftop terrace", "gym", "doorman", "wifi", "smart home", "wine cooler"]),
            price_range=json.dumps({"min": 7000, "max": 10000}),
            bedroom_count=3,
            bathroom_count=3,
            max_guests=6,
            is_active=True,
            created_at=datetime.utcnow() - timedelta(days=22)
        ),
        Villa(
            id=4,
            name="Tropical Paradise",
            location="Maui, Hawaii",
            description="Private villa with infinity pool overlooking the ocean",
            amenities=json.dumps(["infinity pool", "outdoor kitchen", "beachfront", "wifi", "massage room", "bbq"]),
            price_range=json.dumps({"min": 6000, "max": 9000}),
            bedroom_count=6,
            bathroom_count=5,
            max_guests=12,
            is_active=True,
            created_at=datetime.utcnow() - timedelta(days=18)
        ),
        Villa(
            id=5,
            name="Historic Manor",
            location="Cotswolds, UK",
            description="17th century manor with period features",
            amenities=json.dumps(["gardens", "library", "wine cellar", "wifi", "fireplaces", "tennis court"]),
            price_range=json.dumps({"min": 3500, "max": 5500}),
            bedroom_count=8,
            bathroom_count=6,
            max_guests=16,
            is_active=True,
            created_at=datetime.utcnow() - timedelta(days=15)
        ),
    ]
    
    session.add_all(villas)
    session.commit()
    print(f"Created {len(villas)} villas")
    return villas


def create_knowledge_sources(session: Session):
    """Create synthetic knowledge sources."""
    knowledge_sources = [
        KnowledgeSource(
            id=1,
            title="Villa Booking Policies",
            source_type="policy_document",
            content_text="All villa bookings require a 50% deposit upon reservation. Cancellation policies vary by season: high season requires 90-day notice for full refund, low season requires 30-day notice. Additional guests beyond max capacity incur $250 per person per night.",
            source_url="https://internal.cvvillas.com/policies/booking",
            embedding_vector=None,  # Will be populated by embedding worker
            is_active=True,
            created_at=datetime.utcnow() - timedelta(days=27)
        ),
        KnowledgeSource(
            id=2,
            title="Amenities Guide",
            source_type="manual",
            content_text="Our premium villas include high-speed wifi, air conditioning, fully equipped kitchens, and weekly housekeeping. Additional services like private chefs, chauffeurs, and spa treatments can be arranged at extra cost. Check individual villa listings for specific amenities.",
            source_url="https://internal.cvvillas.com/manuals/amenities",
            embedding_vector=None,
            is_active=True,
            created_at=datetime.utcnow() - timedelta(days=24)
        ),
        KnowledgeSource(
            id=3,
            title="Check-in/Check-out Procedures",
            source_type="procedure",
            content_text="Standard check-in time is 4:00 PM local time. Check-out time is 11:00 AM. Late check-out requests must be approved 24 hours in advance and may incur additional charges. Early check-in is subject to availability.",
            source_url="https://internal.cvvillas.com/procedures/checkin",
            embedding_vector=None,
            is_active=True,
            created_at=datetime.utcnow() - timedelta(days=21)
        ),
        KnowledgeSource(
            id=4,
            title="Seasonal Pricing Guide",
            source_type="pricing",
            content_text="Prices vary by season: Peak season (Dec 20-Jan 5, July-August) rates are 30% higher. Shoulder season (April-June, Sept-Oct) rates are standard. Low season (Nov-March excluding holidays) offers 15% discounts.",
            source_url="https://internal.cvvillas.com/pricing/seasons",
            embedding_vector=None,
            is_active=True,
            created_at=datetime.utcnow() - timedelta(days=18)
        ),
        KnowledgeSource(
            id=5,
            title="Safety and Emergency Procedures",
            source_type="safety",
            content_text="All villas are equipped with fire extinguishers, smoke detectors, and first aid kits. Emergency contact numbers are posted in each villa. In case of medical emergency, call 911 (US) or equivalent local number. Contact villa manager for non-emergency issues.",
            source_url="https://internal.cvvillas.com/safety/emergency",
            embedding_vector=None,
            is_active=True,
            created_at=datetime.utcnow() - timedelta(days=15)
        ),
    ]
    
    session.add_all(knowledge_sources)
    session.commit()
    print(f"Created {len(knowledge_sources)} knowledge sources")
    return knowledge_sources


def create_answers_and_citations(session: Session, users, knowledge_sources):
    """Create synthetic answers with citations."""
    answers = [
        Answer(
            id=1,
            user_id=3,  # agent1
            question_text="What is the cancellation policy during high season?",
            answer_text="During high season, which includes December 20 through January 5, you must provide at least 90 days notice for a full refund.",
            confidence_score=0.85,
            created_at=datetime.utcnow() - timedelta(days=10)
        ),
        Answer(
            id=2,
            user_id=4,  # agent2
            question_text="What time is check-in and check-out?",
            answer_text="Standard check-in time is 4:00 PM local time, and check-out is at 11:00 AM. Late check-out requests require 24-hour advance approval.",
            confidence_score=0.92,
            created_at=datetime.utcnow() - timedelta(days=8)
        ),
        Answer(
            id=3,
            user_id=3,  # agent1
            question_text="Are extra guests allowed and what's the cost?",
            answer_text="Yes, additional guests beyond the maximum capacity are permitted at an extra cost of $250 per person per night.",
            confidence_score=0.78,
            created_at=datetime.utcnow() - timedelta(days=5)
        ),
    ]
    
    session.add_all(answers)
    session.commit()
    
    # Create citations for answers
    citations = [
        Citation(
            answer_id=1,
            knowledge_source_id=1,
            snippet_text="high season requires 90-day notice for full refund",
            relevance_score=0.95,
            created_at=datetime.utcnow() - timedelta(days=10)
        ),
        Citation(
            answer_id=2,
            knowledge_source_id=3,
            snippet_text="Standard check-in time is 4:00 PM local time. Check-out time is 11:00 AM.",
            relevance_score=0.98,
            created_at=datetime.utcnow() - timedelta(days=8)
        ),
        Citation(
            answer_id=3,
            knowledge_source_id=1,
            snippet_text="Additional guests beyond max capacity incur $250 per person per night.",
            relevance_score=0.92,
            created_at=datetime.utcnow() - timedelta(days=5)
        ),
    ]
    
    session.add_all(citations)
    session.commit()
    print(f"Created {len(answers)} answers with {len(citations)} citations")
    return answers, citations


def create_expert_corrections(session: Session, answers, users):
    """Create synthetic expert corrections."""
    corrections = [
        ExpertCorrection(
            id=1,
            answer_id=3,
            corrected_by_user_id=2,  # expert user
            correction_text="The cost for additional guests is actually tiered: $250 for adults, $150 for children under 12.",
            status="approved",
            created_at=datetime.utcnow() - timedelta(days=4),
            reviewed_at=datetime.utcnow() - timedelta(days=3),
            reviewed_by_user_id=1  # admin
        ),
        ExpertCorrection(
            id=2,
            answer_id=1,
            corrected_by_user_id=2,  # expert user
            correction_text="High season cancellation window is actually 120 days for villas booked over holiday periods.",
            status="pending",
            created_at=datetime.utcnow() - timedelta(days=2)
        ),
    ]
    
    session.add_all(corrections)
    session.commit()
    print(f"Created {len(corrections)} expert corrections")
    return corrections


def create_coverage_gaps(session: Session):
    """Create synthetic coverage gaps."""
    coverage_gaps = [
        CoverageGap(
            id=1,
            question_text="Are pets allowed in the villas?",
            occurrence_count=5,
            first_occurred_at=datetime.utcnow() - timedelta(days=7),
            last_occurred_at=datetime.utcnow() - timedelta(days=1),
            assigned_to_user_id=2,  # expert
            status="open",
            created_at=datetime.utcnow() - timedelta(days=7)
        ),
        CoverageGap(
            id=2,
            question_text="What is the policy for damages or breakages?",
            occurrence_count=3,
            first_occurred_at=datetime.utcnow() - timedelta(days=5),
            last_occurred_at=datetime.utcnow() - timedelta(days=2),
            assigned_to_user_id=None,
            status="unassigned",
            created_at=datetime.utcnow() - timedelta(days=5)
        ),
    ]
    
    session.add_all(coverage_gaps)
    session.commit()
    print(f"Created {len(coverage_gaps)} coverage gaps")
    return coverage_gaps


def create_escalations(session: Session, users):
    """Create synthetic escalations."""
    escalations = [
        Escalation(
            id=1,
            answer_id=3,
            escalated_by_user_id=3,  # agent1
            reason="Customer dispute about pricing accuracy",
            status="resolved",
            resolved_at=datetime.utcnow() - timedelta(days=3),
            resolved_by_user_id=2,  # expert
            created_at=datetime.utcnow() - timedelta(days=4)
        ),
        Escalation(
            id=2,
            answer_id=1,
            escalated_by_user_id=4,  # agent2
            reason="Complex booking requiring manual review",
            status="open",
            created_at=datetime.utcnow() - timedelta(days=2)
        ),
    ]
    
    session.add_all(escalations)
    session.commit()
    print(f"Created {len(escalations)} escalations")
    return escalations


def create_agent_plans(session: Session, users):
    """Create synthetic agent plans."""
    plans = [
        AgentPlan(
            id=1,
            user_id=3,  # agent1
            plan_type="premium",
            monthly_question_limit=1000,
            used_questions=247,
            expires_at=datetime.utcnow() + timedelta(days=60),
            created_at=datetime.utcnow() - timedelta(days=20)
        ),
        AgentPlan(
            id=2,
            user_id=4,  # agent2
            plan_type="basic",
            monthly_question_limit=500,
            used_questions=183,
            expires_at=datetime.utcnow() + timedelta(days=45),
            created_at=datetime.utcnow() - timedelta(days=15)
        ),
    ]
    
    session.add_all(plans)
    session.commit()
    print(f"Created {len(plans)} agent plans")
    return plans


def create_configurations(session: Session):
    """Create system configurations."""
    configurations = [
        Configuration(
            id=1,
            key="similarity_threshold",
            value="0.7",
            description="Minimum similarity score for knowledge source retrieval",
            is_active=True,
            created_at=datetime.utcnow() - timedelta(days=30)
        ),
        Configuration(
            id=2,
            key="max_citations_per_answer",
            value="5",
            description="Maximum number of citations to include per answer",
            is_active=True,
            created_at=datetime.utcnow() - timedelta(days=30)
        ),
        Configuration(
            id=3,
            key="low_confidence_threshold",
            value="0.6",
            description="Confidence score below which answers are flagged for review",
            is_active=True,
            created_at=datetime.utcnow() - timedelta(days=30)
        ),
        Configuration(
            id=4,
            key="auto_escalate_threshold",
            value="3",
            description="Number of times a question must fail before auto-escalation",
            is_active=True,
            created_at=datetime.utcnow() - timedelta(days=30)
        ),
    ]
    
    session.add_all(configurations)
    session.commit()
    print(f"Created {len(configurations)} configurations")
    return configurations


def create_audit_logs(session: Session, users):
    """Create synthetic audit logs."""
    now = datetime.utcnow()
    audit_logs = [
        AuditLog(
            user_id=1,
            action="login",
            resource_type="user",
            resource_id=1,
            ip_address="192.168.1.100",
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
            timestamp=now - timedelta(hours=2)
        ),
        AuditLog(
            user_id=3,
            action="create_answer",
            resource_type="answer",
            resource_id=1,
            ip_address="192.168.1.101",
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            timestamp=now - timedelta(days=1)
        ),
        AuditLog(
            user_id=2,
            action="submit_correction",
            resource_type="expert_correction",
            resource_id=1,
            ip_address="192.168.1.102",
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 14_0)",
            timestamp=now - timedelta(days=3)
        ),
        AuditLog(
            user_id=4,
            action="escalate",
            resource_type="escalation",
            resource_id=2,
            ip_address="192.168.1.103",
            user_agent="Mozilla/5.0 (Linux; Android 11)",
            timestamp=now - timedelta(days=2)
        ),
    ]
    
    session.add_all(audit_logs)
    session.commit()
    print(f"Created {len(audit_logs)} audit logs")
    return audit_logs


def seed_database():
    """Main seeding function."""
    session = SessionLocal()
    
    try:
        print("Starting database seeding...")
        
        # Clear existing data (for idempotent seeding)
        print("Clearing existing data...")
        session.query(AuditLog).delete()
        session.query(Configuration).delete()
        session.query(AgentPlan).delete()
        session.query(Escalation).delete()
        session.query(CoverageGap).delete()
        session.query(ExpertCorrection).delete()
        session.query(Citation).delete()
        session.query(Answer).delete()
        session.query(KnowledgeSource).delete()
        session.query(Villa).delete()
        session.query(User).delete()
        session.commit()
        print("Existing data cleared")
        
        # Create new data
        users = create_users(session)
        villas = create_villas(session)
        knowledge_sources = create_knowledge_sources(session)
        answers, citations = create_answers_and_citations(session, users, knowledge_sources)
        corrections = create_expert_corrections(session, answers, users)
        coverage_gaps = create_coverage_gaps(session)
        escalations = create_escalations(session, users)
        plans = create_agent_plans(session, users)
        configurations = create_configurations(session)
        audit_logs = create_audit_logs(session, users)
        
        print("\nDatabase seeding completed successfully!")
        print(f"Total records created: {len(users)} users, {len(villas)} villas, {len(knowledge_sources)} knowledge sources")
        print(f"  {len(answers)} answers with {len(citations)} citations")
        print(f"  {len(corrections)} corrections, {len(coverage_gaps)} coverage gaps")
        print(f"  {len(escalations)} escalations, {len(plans)} agent plans")
        print(f"  {len(configurations)} configurations, {len(audit_logs)} audit logs")
        
    except Exception as e:
        session.rollback()
        print(f"Error seeding database: {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    seed_database()