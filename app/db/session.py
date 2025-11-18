from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession, 
    create_async_engine,
    async_sessionmaker
)

from app.core.config import settings

# Create the asynchronous database engine
# We use the DATABASE_URL defined in config which uses the 'asyncpg' driver
engine = create_async_engine(
    settings.DATABASE_URL, 
    echo=True, # Set to False in production
)

# Define a factory for creating new AsyncSession objects
# autoflush=False and expire_on_commit=False are recommended for async sessions
AsyncSessionLocal = async_sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    autoflush=False, 
    expire_on_commit=False
)

# Dependency to provide a database session for FastAPI endpoints
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency function that yields an asynchronous database session.
    The session is automatically closed upon completion.
    """
    async with AsyncSessionLocal() as session:
        yield session