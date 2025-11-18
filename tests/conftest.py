import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import NullPool
from typing import AsyncGenerator

# Import Base and the main FastAPI app
from app.db.base_class import Base
from app.db.session import get_db
from app.main import app
from app.models.user import User
from app.core import security
from app.core.config import settings

ASYNC_DB_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(
    ASYNC_DB_URL, 
    echo=False, 
    poolclass=NullPool
)

TestAsyncSessionLocal = async_sessionmaker(
    bind=test_engine, 
    class_=AsyncSession, 
    autoflush=False, 
    expire_on_commit=False
)


@pytest_asyncio.fixture
async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency that yields a session for the test database."""
    async with TestAsyncSessionLocal() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db


@pytest_asyncio.fixture(scope="session")
def anyio_backend():
    return 'asyncio'

@pytest_asyncio.fixture(scope="session")
async def client() -> AsyncGenerator[AsyncClient, None]:
    """Asynchronous test client for API requests."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def db_session() -> AsyncSession:
    """Provides a fresh database session for setup/teardown within a test."""
    async with TestAsyncSessionLocal() as session:
        yield session

async def create_test_user(session: AsyncSession, email: str, role: str) -> User:
    """Helper to create a user for testing authentication."""
    user = User(
        email=email,
        hashed_password=security.get_password_hash("testpassword"),
        role=role
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

@pytest_asyncio.fixture
async def normal_user(db_session: AsyncSession) -> User:
    """Fixture for a standard 'user'."""
    return await create_test_user(db_session, "user@test.com", "user")

@pytest_asyncio.fixture
async def admin_user(db_session: AsyncSession) -> User:
    """Fixture for an 'admin' user."""
    return await create_test_user(db_session, "admin@test.com", "admin")

@pytest_asyncio.fixture
async def user_token(client: AsyncClient, normal_user: User) -> str:
    """Login and return the JWT token for a normal user."""
    response = await client.post(
        f"{settings.API_V1_STR}/auth/login",
        data={"username": "user@test.com", "password": "testpassword"}
    )
    return response.json()["access_token"]

@pytest_asyncio.fixture
async def admin_token(client: AsyncClient, admin_user: User) -> str:
    """Login and return the JWT token for an admin user."""
    response = await client.post(
        f"{settings.API_V1_STR}/auth/login",
        data={"username": "admin@test.com", "password": "testpassword"}
    )
    return response.json()["access_token"]