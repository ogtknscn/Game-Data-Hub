"""
Authentication service
"""
from typing import Optional
from datetime import timedelta
from app.core.security import verify_password, get_password_hash, create_access_token
from app.core.config import get_settings
from app.domain.interfaces.services import IAuthService
from app.infrastructure.models.user import UserModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

settings = get_settings()


class AuthService(IAuthService):
    """Authentication service implementation"""
    
    def __init__(self, session: Optional[AsyncSession] = None):
        self.session = session
    
    async def authenticate(self, username: str, password: str) -> Optional[str]:
        """Authenticate user and return JWT token"""
        if not self.session:
            return None
        
        # Get user by username
        stmt = select(UserModel).where(UserModel.username == username)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()
        
        if not user or not user.is_active:
            return None
        
        # Verify password
        if not verify_password(password, user.hashed_password):
            return None
        
        # Create access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        token_data = {"sub": str(user.id), "username": user.username}
        access_token = create_access_token(data=token_data, expires_delta=access_token_expires)
        
        return access_token
    
    async def register(self, username: str, email: str, password: str) -> dict:
        """Register new user"""
        if not self.session:
            raise ValueError("Database session not available")
        
        # Check if user exists
        stmt = select(UserModel).where(
            (UserModel.username == username) | (UserModel.email == email)
        )
        result = await self.session.execute(stmt)
        existing_user = result.scalar_one_or_none()
        
        if existing_user:
            raise ValueError("Username or email already exists")
        
        # Create new user
        hashed_password = get_password_hash(password)
        new_user = UserModel(
            username=username,
            email=email,
            hashed_password=hashed_password,
            is_active=True
        )
        
        self.session.add(new_user)
        await self.session.flush()
        await self.session.refresh(new_user)
        # Note: commit will be done by get_db dependency
        
        return {
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email
        }

