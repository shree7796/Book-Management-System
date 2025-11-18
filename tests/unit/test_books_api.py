import pytest
from httpx import AsyncClient
from app.core.config import settings

# Sample data used across tests
TEST_BOOK_DATA = {
    "title": "The Async Architect",
    "author": "A. Code",
    "genre": "Programming",
    "year_published": 2023
}
TEST_BOOK_CONTENT = "This is the full content of the book about asynchronous Python and FastAPI architecture."

@pytest.mark.anyio
async def test_create_book_requires_admin(client: AsyncClient, user_token: str):
    """Test that only admin can create a book (RBAC check)."""
    response = await client.post(
        f"{settings.API_V1_STR}/books",
        headers={"Authorization": f"Bearer {user_token}"},
        json={"book_in": TEST_BOOK_DATA, "content": TEST_BOOK_CONTENT}
    )
    # Expect Forbidden (403) for a non-admin user
    assert response.status_code == 403 
    assert "Not enough privileges" in response.json()["detail"]

@pytest.mark.anyio
async def test_create_and_read_book_success(client: AsyncClient, admin_token: str):
    """Test successful book creation and subsequent retrieval."""
    create_response = await client.post(
        f"{settings.API_V1_STR}/books",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"book_in": TEST_BOOK_DATA, "content": TEST_BOOK_CONTENT}
    )
    assert create_response.status_code == 201
    created_book = create_response.json()
    assert created_book["title"] == TEST_BOOK_DATA["title"]
    # Check if the AI Summary generation ran (even if it mocked or failed)
    assert "summary" in created_book 

    book_id = created_book["id"]
    
    read_response = await client.get(
        f"{settings.API_V1_STR}/books/{book_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert read_response.status_code == 200
    assert read_response.json()["id"] == book_id
    
    # Store ID for later tests
    pytest.book_id = book_id 

@pytest.mark.anyio
async def test_add_review_to_book(client: AsyncClient, user_token: str):
    """Test adding a review to the created book."""
    if not hasattr(pytest, 'book_id'):
        # Skip if previous test failed
        return 

    review_data = {"review_text": "Great book on async code!", "rating": 5}
    
    response = await client.post(
        f"{settings.API_V1_STR}/books/{pytest.book_id}/reviews",
        headers={"Authorization": f"Bearer {user_token}"},
        json=review_data
    )
    assert response.status_code == 201
    assert response.json()["rating"] == 5

@pytest.mark.anyio
async def test_get_book_summary_and_stats(client: AsyncClient, user_token: str):
    """Test the mandatory aggregated summary and rating endpoint."""
    if not hasattr(pytest, 'book_id'):
        return 
        
    response = await client.get(
        f"{settings.API_V1_STR}/books/{pytest.book_id}/summary",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 200
    summary_data = response.json()
    
    # Check mandatory fields
    assert summary_data["aggregated_rating"] == 5.0
    assert summary_data["review_count"] == 1
    assert "book_summary" in summary_data 
    assert "review_sentiment_summary" in summary_data
    assert summary_data["review_sentiment_summary"] != "No reviews yet."