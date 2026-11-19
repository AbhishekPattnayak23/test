"""
Auth0 JWT validation service and RBAC dependency injection.
Handles authentication, token validation, and role-based access control.
"""

import os
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Configuration
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "development-secret-key-change-in-production")
JWT_ALGORITHM = "HS256"
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

# Auth0-style configuration (can be extended for production)
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", "https://cvvillas.eu.auth0.com/")
AUTH0_API_AUDIENCE = os.getenv("AUTH0_API_AUDIENCE", "cv-villas-api")

# Security scheme
security = HTTPBearer()


class UserTokenData:
    """User data extracted from JWT token."""
    
    def __init__(self, user_id: str, email: str, role: str, **kwargs):
        self.user_id = user_id
        self.email = email
        self.role = role
        self.scopes = kwargs.get("scopes", [])
        self.permissions = kwargs.get("permissions", [])
    
    def __repr__(self):
        return f"UserTokenData(user_id={self.user_id}, email={self.email}, role={self.role})"


class AuthService:
    """Authentication and authorization service."""
    
    def __init__(self):
        self.secret_key = JWT_SECRET_KEY
        self.algorithm = JWT_ALGORITHM
    
    def decode_token(self, token: str) -> Dict[str, Any]:
        """
        Decode and validate JWT token.
        
        Args:
            token: JWT token string
            
        Returns:
            Decoded token payload
            
        Raises:
            HTTPException: If token is invalid or expired
        """
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm]
            )
            return payload
        except JWTError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid authentication credentials: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Token validation failed: {str(e)}"
            )
    
    def extract_user_data(self, token_payload: Dict[str, Any]) -> UserTokenData:
        """
        Extract user data from token payload.
        
        Args:
            token_payload: Decoded JWT payload
            
        Returns:
            UserTokenData object
            
        Raises:
            HTTPException: If required fields are missing
        """
        try:
            user_id = token_payload.get("sub")
            email = token_payload.get("email")
            role = token_payload.get("role", "guest")
            
            if not user_id:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token missing user identifier (sub)"
                )
            
            if not email:
                email = token_payload.get("preferred_username") or f"user-{user_id}"
            
            return UserTokenData(
                user_id=user_id,
                email=email,
                role=role,
                scopes=token_payload.get("scopes", []),
                permissions=token_payload.get("permissions", [])
            )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Failed to extract user data from token: {str(e)}"
            )
    
    def create_access_token(self, user_data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """
        Create a JWT access token for development/testing.
        
        Args:
            user_data: User data to encode in token
            expires_delta: Optional token expiry time
            
        Returns:
            JWT token string
        """
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode = user_data.copy()
        to_encode.update({
            "exp": expire,
            "iat": datetime.utcnow(),
            "iss": AUTH0_DOMAIN,
            "aud": AUTH0_API_AUDIENCE
        })
        
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def verify_role(self, user_data: UserTokenData, allowed_roles: List[str]) -> bool:
        """
        Verify if user has one of the allowed roles.
        
        Args:
            user_data: User token data
            allowed_roles: List of allowed roles
            
        Returns:
            True if user has an allowed role, False otherwise
        """
        return user_data.role in allowed_roles
    
    def verify_scopes(self, user_data: UserTokenData, required_scopes: List[str]) -> bool:
        """
        Verify if user has all required scopes.
        
        Args:
            user_data: User token data
            required_scopes: List of required scopes
            
        Returns:
            True if user has all required scopes, False otherwise
        """
        return all(scope in user_data.scopes for scope in required_scopes)
    
    def verify_permissions(self, user_data: UserTokenData, required_permissions: List[str]) -> bool:
        """
        Verify if user has all required permissions.
        
        Args:
            user_data: User token data
            required_permissions: List of required permissions
            
        Returns:
            True if user has all required permissions, False otherwise
        """
        return all(permission in user_data.permissions for permission in required_permissions)


# Dependency injection functions
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> UserTokenData:
    """
    Dependency to get current authenticated user.
    
    Args:
        credentials: HTTP authorization credentials
        
    Returns:
        UserTokenData object
        
    Raises:
        HTTPException: If authentication fails
    """
    auth_service = AuthService()
    token = credentials.credentials
    payload = auth_service.decode_token(token)
    return auth_service.extract_user_data(payload)


def require_role(allowed_roles: List[str]):
    """
    Dependency factory to require specific roles.
    
    Args:
        allowed_roles: List of allowed roles
        
    Returns:
        Dependency function
    """
    def role_checker(
        current_user: UserTokenData = Depends(get_current_user)
    ):
        auth_service = AuthService()
        if not auth_service.verify_role(current_user, allowed_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{current_user.role}' not allowed. Required roles: {allowed_roles}"
            )
        return current_user
    return role_checker


def require_scopes(required_scopes: List[str]):
    """
    Dependency factory to require specific scopes.
    
    Args:
        required_scopes: List of required scopes
        
    Returns:
        Dependency function
    """
    def scope_checker(
        current_user: UserTokenData = Depends(get_current_user)
    ):
        auth_service = AuthService()
        if not auth_service.verify_scopes(current_user, required_scopes):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient scopes. Required scopes: {required_scopes}"
            )
        return current_user
    return scope_checker


def require_permissions(required_permissions: List[str]):
    """
    Dependency factory to require specific permissions.
    
    Args:
        required_permissions: List of required permissions
        
    Returns:
        Dependency function
    """
    def permission_checker(
        current_user: UserTokenData = Depends(get_current_user)
    ):
        auth_service = AuthService()
        if not auth_service.verify_permissions(current_user, required_permissions):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Required permissions: {required_permissions}"
            )
        return current_user
    return permission_checker


# Pre-defined role dependencies for common use cases
require_admin = require_role(["admin"])
require_expert = require_role(["expert", "admin"])
require_agent = require_role(["agent", "expert", "admin"])
require_guest = require_role(["guest", "agent", "expert", "admin"])


# Mock user data for development/testing (when Auth0 is not configured)
class MockAuthService:
    """Mock authentication service for development."""
    
    def __init__(self):
        self.mock_users = {
            "admin": {
                "sub": "auth0|admin123",
                "email": "admin@cvvillas.com",
                "role": "admin",
                "scopes": ["read", "write", "admin"],
                "permissions": ["manage_users", "manage_villas", "view_audit_logs"]
            },
            "expert": {
                "sub": "auth0|expert456",
                "email": "expert@cvvillas.com",
                "role": "expert",
                "scopes": ["read", "write"],
                "permissions": ["submit_corrections", "review_answers"]
            },
            "agent": {
                "sub": "auth0|agent789",
                "email": "agent@cvvillas.com",
                "role": "agent",
                "scopes": ["read"],
                "permissions": ["ask_questions", "view_villas"]
            },
            "guest": {
                "sub": "auth0|guest012",
                "email": "guest@example.com",
                "role": "guest",
                "scopes": ["read"],
                "permissions": ["view_public"]
            }
        }
    
    def get_mock_user(self, role: str) -> Dict[str, Any]:
        """Get mock user data for testing."""
        return self.mock_users.get(role, self.mock_users["guest"])
    
    def create_mock_token(self, role: str = "guest") -> str:
        """Create a mock JWT token for development."""
        auth_service = AuthService()
        mock_user = self.get_mock_user(role)
        return auth_service.create_access_token(mock_user)


# Example usage patterns for endpoints:
"""
# In FastAPI endpoint definitions:

from .services.auth import (
    get_current_user, require_admin, require_expert,
    require_agent, require_guest, require_scopes
)

@app.get("/api/admin/users")
async def get_users(current_user: UserTokenData = Depends(require_admin)):
    # Only admin users can access this endpoint
    pass

@app.get("/api/expert/corrections")
async def get_pending_corrections(
    current_user: UserTokenData = Depends(require_expert),
    scopes: UserTokenData = Depends(require_scopes(["read:corrections"]))
):
    # Expert users with specific scope can access
    pass

@app.get("/api/villas")
async def get_villas(current_user: UserTokenData = Depends(require_guest)):
    # All authenticated users (any role) can access
    pass
"""