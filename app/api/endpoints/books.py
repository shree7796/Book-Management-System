from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any

from app.db.session import get_db
from app.schemas.book import Book, BookCreate, BookUpdate
from app.schemas.review import Review, ReviewCreate
from app.services import book_service, review_service
from app.api.dependencies import current_user, current_admin

router = APIRouter()

@router.post("/", response_model=Book, status_code=status.HTTP_201_CREATED, summary="Add a new book (Admin Only)")
async def create_new_book(
    book_in: BookCreate, 
    content: str,
    db: AsyncSession = Depends(get_db),
    # Only allow administrators to add new books (RBAC applied)
    admin_user = Depends(current_admin) 
):
    """
    Adds a new book and asynchronously generates its summary using Llama3.
    Requires 'admin' role.
    """
    return await book_service.create_book(db, book_in, content)

@router.get("/", response_model=List[Book], summary="Retrieve all books")
async def read_books(
    db: AsyncSession = Depends(get_db),
    user = Depends(current_user) # Requires any authenticated user
):
    """
    Retrieves a list of all books in the catalog.
    """
    return await book_service.get_all_books(db, limit=50)

@router.get("/{book_id}", response_model=Book, summary="Retrieve a specific book")
async def read_book(
    book_id: int, 
    db: AsyncSession = Depends(get_db),
    user = Depends(current_user) # Requires any authenticated user
):
    """
    Retrieves a book by its ID.
    """
    book = await book_service.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.put("/{book_id}", response_model=Book, summary="Update a book (Admin Only)")
async def update_book_info(
    book_id: int, 
    book_in: BookUpdate,
    db: AsyncSession = Depends(get_db),
    admin_user = Depends(current_admin) # Requires 'admin' role
):
    """
    Updates the information for an existing book.
    Requires 'admin' role.
    """
    book = await book_service.update_book(db, book_id, book_in)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a book (Admin Only)")
async def delete_existing_book(
    book_id: int,
    db: AsyncSession = Depends(get_db),
    admin_user = Depends(current_admin) # Requires 'admin' role
):
    """
    Deletes a book and its associated reviews.
    Requires 'admin' role.
    """
    success = await book_service.delete_book(db, book_id)
    if not success:
        raise HTTPException(status_code=404, detail="Book not found")
    return 


@router.post("/{book_id}/reviews", response_model=Review, status_code=status.HTTP_201_CREATED, summary="Add a review for a book")
async def add_review_to_book(
    book_id: int,
    review_in: ReviewCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(current_user) # Requires any authenticated user
):
    """
    Adds a new review to a specific book.
    """
    # Verify book exists
    if not await book_service.get_book(db, book_id):
        raise HTTPException(status_code=404, detail="Book not found")
    
    return await review_service.create_review(db, book_id, current_user.id, review_in)

@router.get("/{book_id}/reviews", response_model=List[Review], summary="Retrieve all reviews for a book")
async def read_reviews_for_book(
    book_id: int,
    db: AsyncSession = Depends(get_db),
    user = Depends(current_user) # Requires any authenticated user
):
    """
    Retrieves all reviews associated with a specific book ID.
    """
    return await review_service.get_reviews_by_book_id(db, book_id)


@router.get("/{book_id}/summary", summary="Get a summary and aggregated rating for a book")
async def get_book_summary_and_stats(
    book_id: int,
    db: AsyncSession = Depends(get_db),
    user = Depends(current_user) # Requires any authenticated user
) -> Dict[str, Any]:
    """
    Returns the Llama3-generated book summary, the aggregated user rating, 
    and a Llama3-generated summary of all user reviews.
    """
    stats = await book_service.get_summary_and_rating(db, book_id)
    if stats is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return stats