import pytest
import asyncio
from typing import AsyncGenerator, Generator
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from tests.test_app import test_app
from app.db.session import get_db
from app.db.base import Base
from app.schemas.user import UserCreate, UserRole
from app.services.user_service import UserService


# Test database URL - Use SQLite for testing
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Create test engine
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    echo=False,  # Disable SQL logging for tests
)

# Create test session
TestingSessionLocal = sessionmaker(
    test_engine, class_=AsyncSession, expire_on_commit=False
)


@pytest.fixture(scope="function")
async def test_db_setup():
    """Set up test database."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def db_session(test_db_setup) -> AsyncGenerator[AsyncSession, None]:
    """Create a test database session."""
    async with TestingSessionLocal() as session:
        yield session


@pytest.fixture
async def client(db_session: AsyncSession) -> TestClient:
    """Create a test client with database session."""
    async def override_get_db():
        yield db_session
    
    test_app.dependency_overrides[get_db] = override_get_db
    
    # Create a test client without startup events
    with TestClient(test_app) as test_client:
        yield test_client
    
    test_app.dependency_overrides.clear()


@pytest.fixture
async def admin_user(db_session: AsyncSession):
    """Create an admin user for testing."""
    from app.models.department import Department
    
    # First create a department
    department = Department(title="Admin Test Department", description="Test department for testing")
    db_session.add(department)
    await db_session.commit()
    await db_session.refresh(department)
    
    user_service = UserService(db_session)
    admin_data = UserCreate(
        email="admin@test.com",
        username="admin",
        password="admin123",
        role=UserRole.admin,
        department_id=department.id
    )
    admin = await user_service.create_user(admin_data)
    return admin


@pytest.fixture
async def normal_user(db_session: AsyncSession):
    """Create a normal user for testing."""
    from app.models.department import Department
    
    # First create a department
    department = Department(title="Normal Test Department", description="Test department for testing")
    db_session.add(department)
    await db_session.commit()
    await db_session.refresh(department)
    
    user_service = UserService(db_session)
    user_data = UserCreate(
        email="user@test.com",
        username="user",
        password="user123",
        role=UserRole.normal,
        department_id=department.id
    )
    user = await user_service.create_user(user_data)
    return user


@pytest.fixture
async def admin_token(client: TestClient, admin_user):
    """Get admin authentication token."""
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "admin@test.com",
            "password": "admin123"
        }
    )
    return response.json()["access_token"]


@pytest.fixture
async def user_token(client: TestClient, normal_user):
    """Get normal user authentication token."""
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "user@test.com",
            "password": "user123"
        }
    )
    return response.json()["access_token"]


@pytest.fixture
def admin_headers(admin_token):
    """Get headers with admin authentication."""
    return {"Authorization": f"Bearer {admin_token}"}


@pytest.fixture
def user_headers(user_token):
    """Get headers with user authentication."""
    return {"Authorization": f"Bearer {user_token}"}
