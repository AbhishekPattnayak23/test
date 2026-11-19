"""
FastAPI application for CV Villas Knowledge Assistant.
Main entry point for the backend API server.
"""

import logging
import sys
from typing import Optional
from datetime import datetime

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('app.log', mode='a')
    ]
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="CV Villas Knowledge Assistant API",
    description="Backend API for CV Villas Knowledge Assistant - RAG-powered villa rental sales support",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development - restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check response model
class HealthResponse(BaseModel):
    """Health check response model."""
    status: str = Field(..., description="Service status")
    timestamp: datetime = Field(..., description="Current server timestamp")
    version: str = Field(..., description="API version")

# API models for documentation
class ErrorResponse(BaseModel):
    """Standard error response model."""
    detail: str = Field(..., description="Error description")
    status_code: int = Field(..., description="HTTP status code")
    timestamp: datetime = Field(..., description="When the error occurred")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Custom handler for validation errors."""
    logger.warning(f"Validation error for {request.url}: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": exc.errors(),
            "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "timestamp": datetime.utcnow()
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Custom handler for general exceptions."""
    logger.error(f"Unhandled exception for {request.url}: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error",
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "timestamp": datetime.utcnow()
        }
    )


@app.get("/api/health", response_model=HealthResponse, tags=["System"])
async def health_check():
    """
    Health check endpoint.
    
    Returns the current status of the API service.
    """
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow(),
        version="1.0.0"
    )


@app.get("/", tags=["System"])
async def root():
    """
    Root endpoint.
    
    Returns basic API information.
    """
    return {
        "message": "CV Villas Knowledge Assistant API",
        "version": "1.0.0",
        "docs": "/api/docs",
        "health": "/api/health"
    }


@app.get("/api/version", tags=["System"])
async def get_version():
    """
    Get API version information.
    
    Returns detailed version information.
    """
    return {
        "version": "1.0.0",
        "api_name": "CV Villas Knowledge Assistant",
        "description": "RAG-powered villa rental sales support system",
        "contact": {
            "email": "support@cvvillas.com"
        },
        "license": {
            "name": "Proprietary",
            "url": "https://cvvillas.com/license"
        }
    }


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    Middleware to log all incoming requests.
    """
    start_time = datetime.utcnow()
    
    # Log incoming request
    logger.info(f"Incoming request: {request.method} {request.url.path}")
    
    try:
        response = await call_next(request)
        process_time = (datetime.utcnow() - start_time).total_seconds() * 1000
        
        # Log response
        logger.info(
            f"Response: {request.method} {request.url.path} "
            f"Status: {response.status_code} "
            f"Duration: {process_time:.2f}ms"
        )
        
        return response
        
    except Exception as e:
        process_time = (datetime.utcnow() - start_time).total_seconds() * 1000
        logger.error(
            f"Error in request: {request.method} {request.url.path} "
            f"Error: {e} "
            f"Duration: {process_time:.2f}ms"
        )
        raise


if __name__ == "__main__":
    import uvicorn
    
    logger.info("Starting CV Villas Knowledge Assistant API server...")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
        reload=True  # Enable auto-reload for development
    )