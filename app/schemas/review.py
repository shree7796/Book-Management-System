from pydantic import BaseModel, Field
from typing import Optional

class ReviewBase(BaseModel):
    review_text: Optional[str] = None
    rating: int = Field(..., ge=1, le=5, description="Rating must be between 1 and 5.")

class ReviewCreate(ReviewBase):
    # book_id will be passed in the URL path, not in the body
    pass 

class Review(ReviewBase):
    id: int
    book_id: int
    user_id: int

    class Config:
        from_attributes = True