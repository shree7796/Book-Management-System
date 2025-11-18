from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.review import Review
from app.schemas.review import ReviewCreate

async def get_reviews_by_book_id(db: AsyncSession, book_id: int, skip: int = 0, limit: int = 100) -> List[Review]:
    """Retrieve all reviews for a specific book."""
    stmt = select(Review).where(Review.book_id == book_id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return list(result.scalars().all())

async def create_review(db: AsyncSession, book_id: int, user_id: int, review_in: ReviewCreate) -> Review:
    """Add a new review for a book."""
    
    db_review = Review(
        book_id=book_id,
        user_id=user_id,
        review_text=review_in.review_text,
        rating=review_in.rating
    )
    
    db.add(db_review)
    await db.commit()
    await db.refresh(db_review)
    return db_review