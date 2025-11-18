from typing import Generator, Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.core import security
from app.core.config import settings
from app.schemas.token import TokenPayload
from app.models.user import User
from app.services import user_service

# OAuth2PasswordBearer is used for handling token extraction from the 'Authorization' header
reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login" 
)

# Dependency function to get the current authenticated user
async def get_current_user(
    db: AsyncSession = Depends(get_db),
    token: str = Depends(reusable_oauth2)
) -> User:
    try:
        # Decode the token payload
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if token_data.sub is None:
         raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await db.get(User, token_data.sub)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

# Helper dependency to require a specific role (Role-Based Access Control)
def require_role(role: str):
    """Dependency that checks if the current user has the required role."""
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role != role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Not enough privileges. Required role: {role}",
            )
        return current_user
    return role_checker

# Public dependencies for easy use in endpoints
current_user = Annotated[User, Depends(get_current_user)]
current_admin = Annotated[User, Depends(require_role("admin"))]