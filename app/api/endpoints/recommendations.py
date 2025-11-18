from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.session import get_db
from app.schemas.book import Book
from app.services import book_service
from app.api.dependencies import current_user

router = APIRouter()


@router.get("/", response_model=List[Book], summary="Get book recommendations based on user preferences")
async def get_book_recommendations(
    current_user = Depends(current_user), # Requires any authenticated user
    db: AsyncSession = Depends(get_db)
):
    """
    Provides book recommendations based on user preferences (for prototype, 
    this simply returns the top 3 highly rated books).
    """    
    all_books = await book_service.get_all_books(db, limit=20) 
    
    preferred_genre = "Fantasy" 
    recommendations = [book for book in all_books if book.genre == preferred_genre][:3]

    if not recommendations:
        return all_books[:3] 
        
    return recommendations