from pydantic import BaseModel, Field
from typing import Optional

# Base schema for shared attributes
class BookBase(BaseModel):
    title: str = Field(..., max_length=255)
    author: str = Field(..., max_length=255)
    genre: Optional[str] = None
    year_published: Optional[int] = None

# Schema for creating a book
class BookCreate(BookBase):
    pass

# Schema for updating a book
class BookUpdate(BookBase):
    title: Optional[str] = None
    author: Optional[str] = None

# Schema for reading/response
class Book(BookBase):
    id: int
    summary: Optional[str] = Field(default="Summary pending generation.")
    
    class Config:
        from_attributes = True