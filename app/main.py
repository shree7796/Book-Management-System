from fastapi import FastAPI
from app.core.config import settings
from app.api.endpoints import auth, books, recommendations, ai_utils
from app.db.base_class import Base
from app.db.session import engine
import asyncio

from app.models import book, review, user 

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

@app.on_event("startup")
async def startup_event():
    # This is useful for initial setup in a development environment.
    # In production, use Alembic for migrations.
    async with engine.begin() as conn:
        # Check if tables exist before creating them
        # Note: This operation can be slow on startup and should be handled by Alembic in a real setup.
        # await conn.run_sync(Base.metadata.drop_all) # Uncomment for clean slate testing
        await conn.run_sync(Base.metadata.create_all)
    
    print("Database tables ensured.")
    
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["Authentication"])
app.include_router(books.router, prefix=f"{settings.API_V1_STR}/books", tags=["Books & Reviews"])
app.include_router(recommendations.router, prefix=f"{settings.API_V1_STR}/recommendations", tags=["Recommendations"])
app.include_router(ai_utils.router, prefix=f"{settings.API_V1_STR}", tags=["AI Utilities"])