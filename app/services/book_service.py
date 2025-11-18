from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, func, desc, update

from app.models.book import Book
from app.models.review import Review
from app.schemas.book import BookCreate, BookUpdate
from app.ai_models.llm_client import llm_client

async def get_book(db: AsyncSession, book_id: int) -> Optional[Book]:
    """Retrieve a single book by ID."""
    return await db.get(Book, book_id)

async def get_all_books(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Book]:
    """Retrieve all books."""
    result = await db.execute(select(Book).offset(skip).limit(limit))
    return list(result.scalars().all())

async def create_book(db: AsyncSession, book_in: BookCreate, content: str) -> Book:
    """Create a new book and asynchronously generate its summary."""
    
    # Asynchronously generate summary using the Llama3 client
    book_summary = await llm_client.generate_book_summary(content, book_in.title)

    # Create the ORM object
    db_book = Book(
        title=book_in.title,
        author=book_in.author,
        genre=book_in.genre,
        year_published=book_in.year_published,
        summary=book_summary or "Summary generation failed or is pending."
    )
    
    # Commit to the database
    db.add(db_book)
    await db.commit()
    await db.refresh(db_book)
    return db_book

async def update_book(db: AsyncSession, book_id: int, book_in: BookUpdate) -> Optional[Book]:
    """Update a book's information."""
    db_book = await get_book(db, book_id)
    if db_book:
        # Use update statement for efficiency or merge for ORM
        update_data = book_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_book, key, value)
        
        await db.commit()
        await db.refresh(db_book)
    return db_book

async def delete_book(db: AsyncSession, book_id: int) -> bool:
    """Delete a book by ID."""
    await db.execute(delete(Review).where(Review.book_id == book_id))
    
    # Delete the book
    result = await db.execute(delete(Book).where(Book.id == book_id))
    
    if result.rowcount > 0:
        await db.commit()
        return True
    return False

async def get_summary_and_rating(db: AsyncSession, book_id: int) -> Dict[str, Any]:
    """
    Retrieves book summary, calculates aggregated rating, and generates a review summary.
    """
    db_book = await get_book(db, book_id)
    if not db_book:
        return None

    stmt = select(func.avg(Review.rating), func.count(Review.id)).where(Review.book_id == book_id)
    result = await db.execute(stmt)
    avg_rating, review_count = result.one()
    
    avg_rating = round(avg_rating, 2) if avg_rating else 0.0

    # Retrieve Review Texts for AI Summary (limit to recent/relevant ones)
    review_results = await db.execute(
        select(Review.review_text)
        .where(Review.book_id == book_id)
        .order_by(desc(Review.id)) # Get newest reviews
        .limit(20) # Limit the amount of text sent to the LLM
    )
    review_texts = "\n---\n".join([r[0] for r in review_results.all() if r[0]])
    
    review_summary = "No reviews yet."
    if review_texts:
        review_summary = await llm_client.generate_review_summary(review_texts)

    return {
        "title": db_book.title,
        "author": db_book.author,
        "book_summary": db_book.summary,
        "aggregated_rating": avg_rating,
        "review_count": review_count,
        "review_sentiment_summary": review_summary
    }