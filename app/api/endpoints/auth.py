from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.token import Token
from app.schemas.user import UserLogin, UserCreate, User as UserSchema
from app.services import user_service
from app.core import security
from app.core.config import settings

router = APIRouter()

@router.post("/login", response_model=Token)
async def login_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: AsyncSession = Depends(get_db)
):
    """
    OAuth2 compatible token login, returns an access token.
    """
    user = await user_service.get_user_by_email(db, email=form_data.username)
    
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )
    
    # Create JWT Token with user ID (subject) and role (for RBAC)
    access_token = security.create_access_token(
        subject=user.id,
        role=user.role,
        expires_delta=None
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_in: UserCreate, 
    db: AsyncSession = Depends(get_db)
):
    """
    Register a new user (default role: 'user').
    """
    user = await user_service.get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this email already exists."
        )
    
    # We enforce 'user' role for self-registration to prevent immediate admin creation
    user_in.role = "user"
    new_user = await user_service.create_user(db, user_in)
    return new_user