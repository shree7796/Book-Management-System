from pydantic import BaseModel

class Token(BaseModel):
    """Schema for the JWT token response."""
    access_token: str
    token_type: str = "bearer"

class TokenPayload(BaseModel):
    """Schema for the data contained within the JWT token."""
    sub: Optional[int] = None
    role: str