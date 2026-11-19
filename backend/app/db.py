"""
Database connection and session management for CV Villas Agent Assist.
"""
import os
from typing import AsyncGenerator, Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, create_async_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from app.config import settings

# Create synchronous engine for Alembic migrations and synchronous operations
sync_engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.SQL_ECHO,
    pool_pre_ping=True,
    pool_recycle=3600,
)

# Create async engine for FastAPI async operations
if settings.DATABASE_URL.startswith("sqlite"):
    # SQLite requires special handling for async
    async_engine = create_async_engine(
        settings.DATABASE_URL.replace("sqlite://", "sqlite+aiosqlite://"),
        echo=settings.SQL_ECHO,
        connect_args={"check_same_thread": False} if ":///" in settings.DATABASE_URL else {},
        poolclass=StaticPool,
    )
elif settings.DATABASE_URL.startswith("postgresql"):
    # PostgreSQL async engine
    async_engine = create_async_engine(
        settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"),
        echo=settings.SQL_ECHO,
        pool_pre_ping=True,
        pool_recycle=3600,
    )
else:
    # Default async engine for other databases
    async_engine = create_async_engine(
        settings.DATABASE_URL,
        echo=settings.SQL_ECHO,
        pool_pre_ping=True,
        pool_recycle=3600,
    )

# Session factories
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=sync_engine,
    class_=Session,
)

AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


def get_db() -> Generator[Session, None, None]:
    """
    Synchronous database session dependency for FastAPI.
    Yields a SQLAlchemy Session object and ensures it's closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Asynchronous database session dependency for FastAPI async endpoints.
    Yields a SQLAlchemy AsyncSession object and ensures it's closed after use.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


def create_tables():
    """
    Create all tables defined in models.
    Used for testing and development.
    """
    from app.models.base import Base
    Base.metadata.create_all(bind=sync_engine)


def drop_tables():
    """
    Drop all tables defined in models.
    Used for testing.
    """
    from app.models.base import Base
    Base.metadata.drop_all(bind=sync_engine)