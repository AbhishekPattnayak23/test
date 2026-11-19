from datetime import datetime
from typing import Any
from sqlalchemy import DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql import func

class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""
    pass

Base = declarative_base(cls=Base)

def utc_now() -> datetime:
    """Return current UTC datetime."""
    return datetime.utcnow()