from pydantic import BaseModel, EmailStr, Field
from typing import Optional

# Base schema for shared attributes
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    role: str = Field(default="user", description="Role for RBAC: 'admin' or 'user'")

class UserCreate(UserBase):
    email: EmailStr
    password: str = Field(..., min_length=8)
    role: str = "user" # Default role for new signups

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

# Schema for login
class UserLogin(BaseModel):
    email: EmailStr
    password: str