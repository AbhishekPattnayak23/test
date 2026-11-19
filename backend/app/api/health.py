"""
Health check endpoint for CV Villas Agent Assist API.
Provides system status information including database connectivity.
"""
from fastapi import APIRouter, Depends
from typing import Dict, Any
import logging

from ..db import get_async_db, get_db
from ..config import get_settings
from ..vector_store import get_vector_store

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """
    Health check endpoint that verifies:
    - API is running
    - Database is connected
    - Vector store is initialized
    """
    health_status = {
        "status": "healthy",
        "services": {},
        "version": "1.0.0",
        "timestamp": None
    }
    
    import datetime
    
    # Set timestamp
    health_status["timestamp"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    
    # Check database connectivity
    try:
        # Try synchronous connection first
        from sqlalchemy import text
        db = next(get_db())
        result = db.execute(text("SELECT 1"))
        db.close()
        health_status["services"]["database"] = {
            "status": "healthy",
            "type": "postgresql/sqlite"
        }
    except Exception as e:
        logger.warning(f"Database health check failed: {e}")
        health_status["services"]["database"] = {
            "status": "unhealthy",
            "error": str(e)
        }
        health_status["status"] = "degraded"
    
    # Check vector store
    try:
        vector_store = get_vector_store()
        # Call a lightweight method to check if vector store is initialized
        # For FAISS, we can check if index exists or if we can get dimensions
        store_type = vector_store.get_store_type()
        health_status["services"]["vector_store"] = {
            "status": "healthy",
            "type": store_type
        }
    except Exception as e:
        logger.warning(f"Vector store health check failed: {e}")
        health_status["services"]["vector_store"] = {
            "status": "unhealthy",
            "error": str(e)
        }
        health_status["status"] = "degraded"
    
    # Get settings for debugging
    try:
        settings = get_settings()
        health_status["config"] = {
            "environment": "development" if settings.DEBUG else "production",
            "debug": settings.DEBUG,
            "cors_enabled": len(settings.CORS_ORIGINS) > 0
        }
    except Exception as e:
        logger.warning(f"Config health check failed: {e}")
        health_status["config"] = {
            "error": str(e)
        }
        health_status["status"] = "degraded"
    
    return health_status


@router.get("/health/detailed")
async def detailed_health_check() -> Dict[str, Any]:
    """
    Detailed health check with more verbose system information.
    """
    health_status = await health_check()
    
    # Add additional detailed information
    import platform
    import psutil
    import sys
    
    health_status["system"] = {
        "python_version": sys.version,
        "platform": platform.platform(),
        "cpu_count": psutil.cpu_count(),
        "memory_available_gb": psutil.virtual_memory().available / (1024**3),
        "disk_usage_percent": psutil.disk_usage('/').percent
    }
    
    # Add active connections count (mock for now)
    health_status["system"]["active_connections"] = 0
    
    return health_status


@router.get("/health/live")
async def liveness_probe() -> Dict[str, Any]:
    """
    Liveness probe for Kubernetes/container orchestration.
    Minimal check that just returns OK if the service is running.
    """
    return {"status": "alive"}


@router.get("/health/ready")
async def readiness_probe() -> Dict[str, Any]:
    """
    Readiness probe for Kubernetes/container orchestration.
    Checks if the service is ready to accept traffic.
    """
    # Check database
    try:
        from sqlalchemy import text
        db = next(get_db())
        result = db.execute(text("SELECT 1"))
        db.close()
        database_ready = True
    except Exception:
        database_ready = False
    
    # Check vector store
    try:
        vector_store = get_vector_store()
        # Simple check - if vector_store has been initialized
        database_ready = True  # Simplified for now
    except Exception:
        database_ready = False
    
    if database_ready:
        return {"status": "ready"}
    else:
        return {"status": "not ready"}, 503