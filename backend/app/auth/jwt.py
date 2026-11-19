"""
Auth0 JWT validation service and RBAC dependency injection for CV Villas Agent Assist.

This module provides JWT token validation, role-based access control (RBAC),
and FastAPI dependencies for securing endpoints with user roles: guest, agent, expert, admin.
"""
import os
import jwt
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from fastapi import Depends, HTTPException, status, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import logging

from ..db import get_async_db
from ..models.user import User
from ..repositories.user_repository import UserRepository

logger = logging.getLogger(__name__)

security = HTTPBearer()


class TokenData(BaseModel):
    """Pydantic model for decoded JWT token data."""
    sub: str  # Subject (user ID or email)
    email: str
    role: str
    exp: int
    iat: int


class AuthService:
    """Service for handling JWT authentication and authorization."""
    
    def __init__(self):
        self.jwt_secret = os.getenv("JWT_SECRET", "development_secret_key_change_in_production")
        self.jwt_algorithm = os.getenv("JWT_ALGORITHM", "HS256")
        self.token_expire_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
    
    def create_access_token(self, user: User) -> str:
        """Create a JWT access token for a user."""
        payload = {
            "sub": str(user.id),
            "email": user.email,
            "role": user.role.value,
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(minutes=self.token_expire_minutes)
        }
        
        token = jwt.encode(
            payload,
            self.jwt_secret,
            algorithm=self.jwt_algorithm
        )
        return token
    
    def decode_token(self, token: str) -> TokenData:
        """Decode and validate a JWT token."""
        try:
            payload = jwt.decode(
                token,
                self.jwt_secret,
                algorithms=[self.jwt_algorithm]
            )
            
            # Convert datetime objects to timestamps if needed
            if isinstance(payload.get("iat"), datetime):
                payload["iat"] = int(payload["iat"].timestamp())
            if isinstance(payload.get("exp"), datetime):
                payload["exp"] = int(payload["exp"].timestamp())
            
            return TokenData(**payload)
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
    
    def verify_token(self, credentials: HTTPAuthorizationCredentials) -> TokenData:
        """Verify a bearer token from HTTP Authorization header."""
        if credentials.scheme != "Bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication scheme"
            )
        
        return self.decode_token(credentials.credentials)


class CurrentUser:
    """Dependency to get current user from JWT token."""
    
    def __init__(self):
        self.auth_service = AuthService()
    
    async def __call__(
        self,
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db=Depends(get_async_db)
    ) -> User:
        """Get the current authenticated user."""
        token_data = self.auth_service.verify_token(credentials)
        
        # Get user from database
        user_repo = UserRepository(db)
        try:
            user = await user_repo.get_by_email(token_data.email)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User not found"
                )
            
            # Verify role hasn't changed (optional security check)
            if user.role.value != token_data.role:
                logger.warning(f"User role mismatch: DB={user.role}, Token={token_data.role}")
                # Token might be stale, but we'll accept it for now
                # Could optionally refresh token here
            
            return user
        except Exception as e:
            logger.error(f"Error fetching user: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )


def require_role(allowed_roles: List[str]):
    """Factory function to create RBAC dependency for specific roles."""
    
    async def role_checker(
        current_user: User = Depends(CurrentUser())
    ) -> User:
        """Check if user has required role."""
        if current_user.role.value not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Required roles: {allowed_roles}"
            )
        return current_user
    
    return role_checker


# Convenience dependencies for common role combinations
require_guest = require_role(["guest", "agent", "expert", "admin"])
require_agent = require_role(["agent", "expert", "admin"])
require_expert = require_role(["expert", "admin"])
require_admin = require_role(["admin"])


class GuestOnly:
    """Dependency for endpoints that should only be accessible to guests (non-authenticated users)."""
    
    async def __call__(self, request) -> None:
        """Check if no authentication is present."""
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="This endpoint is for guests only"
            )


# Singleton instances for reuse
auth_service = AuthService()
current_user = CurrentUser()