import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi.testclient import TestClient

from app.main import app
from app.api.v1.endpoints.auth import get_db
from app.models.user import User
from app.core.security import get_password_hash


@pytest.fixture
def plain_password():
    """Consistent password for test fixtures."""
    return "ValidPassword123!"


@pytest.fixture
def hashed_password(plain_password):
    """Bcrypt hash for test fixture password."""
    return get_password_hash(plain_password)


@pytest.fixture
def active_user(hashed_password):
    """Active test user instance."""
    return User(
        id=1,
        username="testuser",
        email="testuser@example.com",
        hashed_password=hashed_password,
        is_active=True,
    )


@pytest.fixture
def inactive_user(hashed_password):
    """Inactive test user instance."""
    return User(
        id=2,
        username="inactiveuser",
        email="inactive@example.com",
        hashed_password=hashed_password,
        is_active=False,
    )


@pytest.fixture
def mock_db_session():
    """
    Mock AsyncSession that supports SQLAlchemy query pattern:
    result = await db.execute(...)
    user = result.scalars().first()
    """
    session = AsyncMock()
    result_mock = MagicMock()
    result_mock.scalars.return_value.first.return_value = None
    session.execute.return_value = result_mock
    return session


@pytest.fixture
def client(mock_db_session):
    """
    FastAPI TestClient with get_db dependency overridden to provide mock_db_session.
    Ensures dependency overrides are cleared after test teardown.
    """
    async def override_get_db():
        yield mock_db_session

    app.dependency_overrides[get_db] = override_get_db
    test_client = TestClient(app)
    try:
        yield test_client
    finally:
        app.dependency_overrides.clear()
