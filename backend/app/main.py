"""
FastAPI application entry point with CORS middleware, structured logging,
and health check endpoint.
"""
import logging
from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from typing import Dict, Any

from .config import Settings, get_settings
from .db import get_async_db, create_tables
from .auth.jwt import AuthService, require_role
from .api import health, auth, ask, answers, corrections, knowledge, admin
from .middleware.audit_middleware import AuditMiddleware

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.
    """
    # Startup
    logger.info("Starting CV Villas Agent Assist backend...")
    try:
        # Create database tables if they don't exist
        await create_tables()
        logger.info("Database tables verified/created successfully")
        
        # Initialize vector store
        from .vector_store import get_vector_store
        vector_store = get_vector_store()
        await vector_store.initialize()
        logger.info("Vector store initialized successfully")
        
        yield
        
    except Exception as e:
        logger.error(f"Error during startup: {e}")
        raise
    finally:
        # Shutdown
        logger.info("Shutting down CV Villas Agent Assist backend...")
        # Cleanup resources if needed


def create_application() -> FastAPI:
    """
    Factory function to create and configure the FastAPI application.
    """
    settings = get_settings()
    
    app = FastAPI(
        title="CV Villas Agent Assist API",
        description="Backend API for CV Villas Agent Assist - A grounded knowledge assistant for sales agents",
        version="1.0.0",
        lifespan=lifespan,
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
    )
    
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Add audit logging middleware
    app.add_middleware(AuditMiddleware)
    
    # Include routers
    app.include_router(health.router, prefix="/api", tags=["health"])
    app.include_router(auth.router, prefix="/api/v1", tags=["auth"])
    app.include_router(ask.router, prefix="/api/v1", tags=["ask"])
    app.include_router(answers.router, prefix="/api/v1", tags=["answers"])
    app.include_router(corrections.router, prefix="/api/v1", tags=["corrections"])
    app.include_router(knowledge.router, prefix="/api/v1", tags=["knowledge"])
    app.include_router(admin.router, prefix="/api/v1", tags=["admin"])
    
    # Global exception handler
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled exception: {exc}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "An unexpected error occurred"
                }
            }
        )
    
    return app


# Create the FastAPI application instance
app = create_application()


if __name__ == "__main__":
    import uvicorn
    
    settings = get_settings()
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info"
    )