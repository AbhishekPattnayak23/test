#!/usr/bin/env python3
"""
Database seed script for CV Villas Knowledge Assistant.
Populates the database with synthetic data for development and testing.
"""

import sys
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models import (
    Base, User, Villa, KnowledgeSource, Answer, Citation, 
    ExpertCorrection, AuditLog, CoverageGap, Escalation, 
    AgentPlan, Configuration
)


def create_engine_and_session():
    """Create SQLAlchemy engine and session."""
    # Using SQLite for development - can be changed to PostgreSQL for production
    engine = create_engine("sqlite:///./cv_villas.db")
    Base.metadata.create_all(engine)  # Create tables if they don't exist
    return engine, Session(engine)


def create_users(session: Session) -> Dict[str, User]:
    """Create users with different roles."""
    users = {}
    
    # Admin user
    admin = User(
        email="admin@cvvillas.com",
        username="admin",
        full_name="Admin User",
        role="admin",
        hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # "admin123"
        is_active=True
    )
    session.add(admin)
    users["admin"] = admin
    
    # Expert users
    expert1 = User(
        email="expert1@cvvillas.com",
        username="expert1",
        full_name="Sarah Johnson",
        role="expert",
        hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        is_active=True
    )
    expert2 = User(
        email="expert2@cvvillas.com",
        username="expert2",
        full_name="Michael Chen",
        role="expert",
        hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        is_active=True
    )
    session.add_all([expert1, expert2])
    users["expert1"] = expert1
    users["expert2"] = expert2
    
    # Agent users
    agents = []
    for i in range(5):
        agent = User(
            email=f"agent{i+1}@cvvillas.com",
            username=f"agent{i+1}",
            full_name=f"Agent {i+1}",
            role="agent",
            hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
            is_active=True
        )
        agents.append(agent)
    session.add_all(agents)
    for i, agent in enumerate(agents):
        users[f"agent{i+1}"] = agent
    
    # Guest user
    guest = User(
        email="guest@example.com",
        username="guest",
        full_name="Guest User",
        role="guest",
        hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        is_active=True
    )
    session.add(guest)
    users["guest"] = guest
    
    session.commit()
    return users


def create_villas(session: Session) -> Dict[str, Villa]:
    """Create villa properties."""
    villas = []
    
    villa_data = [
        {
            "name": "Villa Serenity",
            "location": "Marbella, Spain",
            "country": "Spain",
            "region": "Costa del Sol",
            "description": "Luxury villa with panoramic sea views and private pool.",
            "amenities": ["private pool", "jacuzzi", "BBQ area", "wine cellar", "sauna", "home cinema"],
            "price_range_min": 5000,
            "price_range_max": 8000,
            "bedrooms": 5,
            "bathrooms": 4,
            "capacity": 10,
            "images": ["villa1.jpg", "villa2.jpg"]
        },
        {
            "name": "Château Provençal",
            "location": "Provence, France",
            "country": "France",
            "region": "Provence",
            "description": "Traditional French farmhouse with lavender fields and vineyard.",
            "amenities": ["vineyard access", "outdoor kitchen", "tennis court", "bike rentals", "wine tasting"],
            "price_range_min": 4500,
            "price_range_max": 7000,
            "bedrooms": 6,
            "bathrooms": 5,
            "capacity": 12,
            "images": ["villa3.jpg", "villa4.jpg"]
        },
        {
            "name": "Casa del Mar",
            "location": "Algarve, Portugal",
            "country": "Portugal",
            "region": "Algarve",
            "description": "Beachfront villa with direct access to private beach.",
            "amenities": ["private beach", "beach bar", "watersports equipment", "chef service", "massage room"],
            "price_range_min": 6000,
            "price_range_max": 9000,
            "bedrooms": 7,
            "bathrooms": 6,
            "capacity": 14,
            "images": ["villa5.jpg", "villa6.jpg"]
        },
        {
            "name": "Tuscan Dream",
            "location": "Tuscany, Italy",
            "country": "Italy",
            "region": "Tuscany",
            "description": "Historic Italian villa with olive groves and infinity pool.",
            "amenities": ["infinity pool", "olive grove", "cooking classes", "wine cellar", "art studio"],
            "price_range_min": 5500,
            "price_range_max": 8500,
            "bedrooms": 8,
            "bathrooms": 7,
            "capacity": 16,
            "images": ["villa7.jpg", "villa8.jpg"]
        },
        {
            "name": "Bali Haven",
            "location": "Bali, Indonesia",
            "country": "Indonesia",
            "region": "Bali",
            "description": "Tropical villa with rice terrace views and yoga pavilion.",
            "amenities": ["yoga pavilion", "rice terrace", "spa treatments", "bamboo architecture", "cultural tours"],
            "price_range_min": 3000,
            "price_range_max": 5000,
            "bedrooms": 4,
            "bathrooms": 3,
            "capacity": 8,
            "images": ["villa9.jpg", "villa10.jpg"]
        }
    ]
    
    for data in villa_data:
        villa = Villa(**data)
        villas.append(villa)
    
    session.add_all(villas)
    session.commit()
    
    # Create a dictionary with villa names as keys
    villa_dict = {}
    for villa in villas:
        villa_dict[villa.name] = villa
    
    return villa_dict


def create_knowledge_sources(session: Session, villas: Dict[str, Villa]) -> Dict[str, KnowledgeSource]:
    """Create knowledge sources for RAG pipeline."""
    sources = []
    
    # FAQ knowledge sources
    faq_content = [
        {
            "title": "What is the check-in time?",
            "content": "Standard check-in time is 4:00 PM. Early check-in may be available upon request, subject to availability and may incur additional charges.",
            "type": "faq",
            "source_uri": "/faq/checkin"
        },
        {
            "title": "What is the cancellation policy?",
            "content": "Cancellations made more than 30 days before arrival date receive full refund minus booking fee. Cancellations within 14-30 days receive 50% refund. Cancellations within 14 days are non-refundable.",
            "type": "faq",
            "source_uri": "/faq/cancellation"
        },
        {
            "title": "Are pets allowed?",
            "content": "Pets are allowed only in specific pet-friendly villas. An additional pet fee of €50 per pet per stay applies. Maximum 2 pets per villa.",
            "type": "faq",
            "source_uri": "/faq/pets"
        }
    ]
    
    # Policy knowledge sources
    policy_content = [
        {
            "title": "Damage Deposit Policy",
            "content": "A damage deposit of €1000 is required upon check-in. This will be refunded within 7 days of departure if no damages are found.",
            "type": "policy",
            "source_uri": "/policies/damage-deposit"
        },
        {
            "title": "Smoking Policy",
            "content": "Smoking is strictly prohibited inside all villas. Designated smoking areas are available outdoors.",
            "type": "policy",
            "source_uri": "/policies/smoking"
        }
    ]
    
    # Villa-specific knowledge
    villa_keys = list(villas.keys())
    for i, villa_name in enumerate(villa_keys):
        villa = villas[villa_name]
        source = KnowledgeSource(
            villa_id=villa.id,
            type="amenity_detail",
            title=f"{villa_name} - Amenities Guide",
            content=f"Detailed guide to amenities at {villa_name}: {', '.join(villa.amenities if villa.amenities else [])}. Additional services include concierge, daily housekeeping, and chef service.",
            source_uri=f"/villas/{villa.id}/amenities",
            metadata={"villa_id": villa.id, "priority": "high"}
        )
        sources.append(source)
    
    # Add all FAQ and policy content
    for item in faq_content + policy_content:
        source = KnowledgeSource(
            type=item["type"],
            title=item["title"],
            content=item["content"],
            source_uri=item["source_uri"],
            metadata={"category": "general"}
        )
        sources.append(source)
    
    # Region guides
    region_guides = [
        {
            "title": "Costa del Sol Travel Guide",
            "content": "The Costa del Sol region offers beautiful beaches, golf courses, and cultural attractions. Best visited from May to October for warm weather.",
            "type": "region_guide",
            "source_uri": "/guides/costa-del-sol"
        },
        {
            "title": "Provence Market Days",
            "content": "Provence is famous for its weekly markets. Aix-en-Provence market is on Tuesdays, Thursdays, and Saturdays with local produce and crafts.",
            "type": "region_guide",
            "source_uri": "/guides/provence-markets"
        }
    ]
    
    for guide in region_guides:
        source = KnowledgeSource(
            type=guide["type"],
            title=guide["title"],
            content=guide["content"],
            source_uri=guide["source_uri"],
            metadata={"region": guide["title"].split()[0]}
        )
        sources.append(source)
    
    session.add_all(sources)
    session.commit()
    
    # Create a simple dictionary with titles as keys
    source_dict = {}
    for source in sources:
        source_dict[source.title] = source
    
    return source_dict


def create_answers(session: Session, users: Dict[str, User]) -> Dict[str, Answer]:
    """Create sample answers to questions."""
    answers = []
    
    # Questions and answers from agent1
    agent1 = users["agent1"]
    qa_pairs = [
        {
            "question": "What is the check-in time for Villa Serenity?",
            "answer_text": "Standard check-in time is 4:00 PM. Early check-in may be available upon request, subject to availability.",
            "confidence_score": 0.95
        },
        {
            "question": "Are pets allowed at Château Provençal?",
            "answer_text": "Pets are allowed only in specific pet-friendly villas. Please check the villa details for pet policy information.",
            "confidence_score": 0.85
        },
        {
            "question": "What amenities does Casa del Mar offer?",
            "answer_text": "Casa del Mar offers private beach access, beach bar, watersports equipment, chef service, and massage room among its amenities.",
            "confidence_score": 0.90
        }
    ]
    
    for i, qa in enumerate(qa_pairs):
        answer = Answer(
            user_id=agent1.id,
            question=qa["question"],
            answer_text=qa["answer_text"],
            confidence_score=qa["confidence_score"],
            source_type="rag",
            created_at=datetime.now() - timedelta(days=10-i)  # Stagger dates
        )
        answers.append(answer)
    
    # Add some lower confidence answers for testing escalation
    low_conf_answer = Answer(
        user_id=users["agent2"].id,
        question="What are the visa requirements for Bali?",
        answer_text="Visa requirements vary by nationality. Most visitors can obtain visa on arrival for short stays.",
        confidence_score=0.45,  # Low confidence
        source_type="template"
    )
    answers.append(low_conf_answer)
    
    session.add_all(answers)
    session.commit()
    
    # Create dictionary with questions as keys
    answer_dict = {}
    for answer in answers:
        answer_dict[answer.question[:50]] = answer  # Use first 50 chars of question as key
    
    return answer_dict


def create_citations(session: Session, answers: Dict[str, Answer], sources: Dict[str, KnowledgeSource]):
    """Create citations linking answers to knowledge sources."""
    citations = []
    
    # Get some answers and sources
    answer_keys = list(answers.keys())
    source_keys = list(sources.keys())
    
    if not answer_keys or not source_keys:
        return
    
    # Create citations for first answer
    first_answer = answers[answer_keys[0]]
    if "check-in" in first_answer.question.lower():
        # Find check-in related source
        for key in source_keys:
            if "check-in" in sources[key].title.lower():
                citation = Citation(
                    answer_id=first_answer.id,
                    source_id=sources[key].id,
                    excerpt="Standard check-in time is 4:00 PM.",
                    relevance_score=0.95
                )
                citations.append(citation)
                break
    
    # Create citations for second answer
    if len(answer_keys) > 1:
        second_answer = answers[answer_keys[1]]
        if "pets" in second_answer.question.lower():
            # Find pet policy source
            for key in source_keys:
                if "pets" in sources[key].title.lower():
                    citation = Citation(
                        answer_id=second_answer.id,
                        source_id=sources[key].id,
                        excerpt="Pets are allowed only in specific pet-friendly villas.",
                        relevance_score=0.85
                    )
                    citations.append(citation)
                    break
    
    if citations:
        session.add_all(citations)
        session.commit()


def create_expert_corrections(session: Session, answers: Dict[str, Answer], users: Dict[str, User]):
    """Create expert corrections for answers."""
    corrections = []
    
    # Get an answer to correct
    answer_keys = list(answers.keys())
    if not answer_keys:
        return
    
    target_answer = answers[answer_keys[0]]
    expert = users["expert1"]
    
    correction = ExpertCorrection(
        answer_id=target_answer.id,
        corrected_by_user_id=expert.id,
        correction_text="Early check-in is available from 1:00 PM, not just upon request. Standard fee is €50.",
        original_text=target_answer.answer_text,
        reason="Updated with more specific information about early check-in fees.",
        status="approved",
        reviewed_by_user_id=users["admin"].id,
        review_notes="Correction verified against current policy."
    )
    corrections.append(correction)
    
    # Create a pending correction
    if len(answer_keys) > 1:
        second_answer = answers[answer_keys[1]]
        pending_correction = ExpertCorrection(
            answer_id=second_answer.id,
            corrected_by_user_id=users["expert2"].id,
            correction_text="Only small dogs under 15kg are allowed. Pet fee is €75 per stay.",
            original_text=second_answer.answer_text,
            reason="Updated pet policy with weight restrictions.",
            status="pending"
        )
        corrections.append(pending_correction)
    
    if corrections:
        session.add_all(corrections)
        session.commit()


def create_audit_logs(session: Session, users: Dict[str, User]):
    """Create sample audit logs."""
    logs = []
    
    actions = ["login", "create_villa", "update_answer", "submit_correction", "view_report"]
    
    for i, user_key in enumerate(list(users.keys())[:3]):  # Log actions for first 3 users
        user = users[user_key]
        for j in range(2):  # 2 logs per user
            log = AuditLog(
                user_id=user.id,
                action=actions[(i + j) % len(actions)],
                entity_type="user" if j % 2 == 0 else "villa",
                entity_id=100 + i + j,
                ip_address="192.168.1." + str(100 + i),
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"
            )
            logs.append(log)
    
    if logs:
        session.add_all(logs)
        session.commit()


def create_coverage_gaps(session: Session, answers: Dict[str, Answer], users: Dict[str, User]):
    """Create coverage gap records."""
    gaps = []
    
    # Get a low confidence answer
    answer_keys = list(answers.keys())
    if len(answer_keys) >= 4:  # Use the low confidence answer we created earlier
        low_conf_answer = answers[answer_keys[3]]  # Index 3 should be the low confidence one
        gap = CoverageGap(
            answer_id=low_conf_answer.id,
            question=low_conf_answer.question,
            confidence_score=low_conf_answer.confidence_score,
            gap_type="missing_source",
            priority="high",
            status="open",
            assigned_to_user_id=users["expert1"].id,
            resolution_notes="Need to verify current visa requirements for Bali"
        )
        gaps.append(gap)
    
    if gaps:
        session.add_all(gaps)
        session.commit()


def create_escalations(session: Session, answers: Dict[str, Answer], users: Dict[str, User]):
    """Create escalation records."""
    escalations = []
    
    # Get a low confidence answer to escalate
    answer_keys = list(answers.keys())
    if len(answer_keys) >= 4:  # Use the low confidence answer
        low_conf_answer = answers[answer_keys[3]]
        escalation = Escalation(
            answer_id=low_conf_answer.id,
            escalated_by_user_id=users["agent2"].id,  # Agent who asked the question
            escalated_to_user_id=users["expert2"].id,  # Expert assigned
            reason="Low confidence answer requiring expert review",
            status="assigned",
            resolution="Verified visa requirements and updated knowledge base."
        )
        escalations.append(escalation)
    
    if escalations:
        session.add_all(escalations)
        session.commit()


def create_agent_plans(session: Session, users: Dict[str, User]):
    """Create agent plans and preferences."""
    plans = []
    
    # Get agent users
    agent_users = [user for user in users.values() if user.role == "agent"]
    
    for i, agent in enumerate(agent_users[:3]):  # Plans for first 3 agents
        plan = AgentPlan(
            agent_id=agent.id,
            plan_name=f"Sales Plan {i+1}",
            preferences={
                "notification_frequency": "daily",
                "preferred_villa_types": ["beachfront", "luxury"],
                "target_regions": ["Europe", "Asia"]
            },
            targets={
                "monthly_sales_target": 50000 + i*10000,
                "customer_satisfaction_target": 0.95,
                "response_time_target": "2 hours"
            }
        )
        plans.append(plan)
    
    if plans:
        session.add_all(plans)
        session.commit()


def create_configuration(session: Session):
    """Create system configuration settings."""
    configurations = []
    
    config_items = [
        {
            "key": "system.max_answer_length",
            "value": 1000,
            "value_type": "integer",
            "category": "system",
            "description": "Maximum allowed length for generated answers"
        },
        {
            "key": "system.confidence_threshold",
            "value": 0.7,
            "value_type": "float",
            "category": "qa",
            "description": "Minimum confidence score for answers to be automatically accepted"
        },
        {
            "key": "system.auto_escalation_threshold",
            "value": 0.5,
            "value_type": "float",
            "category": "qa",
            "description": "Confidence score below which answers are automatically escalated"
        },
        {
            "key": "email.notifications_enabled",
            "value": True,
            "value_type": "boolean",
            "category": "email",
            "description": "Enable email notifications for system events"
        },
        {
            "key": "security.jwt_expiry_hours",
            "value": 24,
            "value_type": "integer",
            "category": "security",
            "description": "JWT token expiry time in hours"
        }
    ]
    
    for item in config_items:
        config = Configuration(**item)
        configurations.append(config)
    
    if configurations:
        session.add_all(configurations)
        session.commit()


def seed_database():
    """Main function to seed the database with synthetic data."""
    print("Starting database seeding...")
    
    try:
        engine, session_factory = create_engine_and_session()
        session = session_factory
        
        print("Creating users...")
        users = create_users(session)
        print(f"Created {len(users)} users")
        
        print("Creating villas...")
        villas = create_villas(session)
        print(f"Created {len(villas)} villas")
        
        print("Creating knowledge sources...")
        sources = create_knowledge_sources(session, villas)
        print(f"Created {len(sources)} knowledge sources")
        
        print("Creating answers...")
        answers = create_answers(session, users)
        print(f"Created {len(answers)} answers")
        
        print("Creating citations...")
        create_citations(session, answers, sources)
        print("Created citations")
        
        print("Creating expert corrections...")
        create_expert_corrections(session, answers, users)
        print("Created expert corrections")
        
        print("Creating audit logs...")
        create_audit_logs(session, users)
        print("Created audit logs")
        
        print("Creating coverage gaps...")
        create_coverage_gaps(session, answers, users)
        print("Created coverage gaps")
        
        print("Creating escalations...")
        create_escalations(session, answers, users)
        print("Created escalations")
        
        print("Creating agent plans...")
        create_agent_plans(session, users)
        print("Created agent plans")
        
        print("Creating configurations...")
        create_configuration(session)
        print("Created configuration items")
        
        session.close()
        print("Database seeding completed successfully!")
        print(f"Total records created: Approximately {len(users) + len(villas) + len(sources) + len(answers) + 10}")
        
    except Exception as e:
        print(f"Error during database seeding: {e}")
        raise


if __name__ == "__main__":
    seed_database()