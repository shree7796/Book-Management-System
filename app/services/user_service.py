from typing import Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash

async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    """Retrieve a user by their email address."""
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalars().first()

async def create_user(db: AsyncSession, user_in: UserCreate) -> User:
    """Create a new user with a hashed password."""
    hashed_password = get_password_hash(user_in.password)
    
    # Create the User model instance
    db_user = User(
        email=user_in.email,
        hashed_password=hashed_password,
        role=user_in.role
    )
    
    # Add to session and commit
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user