from fastapi.testclient import TestClient
from backend.main import app
from backend.auth import get_current_active_admin_user, get_current_user
from backend.models import User
import pytest

client = TestClient(app)

# Override dependency to simulate an admin user
async def override_get_admin_user():
    return User(username="admin", is_admin=True)

# Override dependency to simulate a regular user
async def override_get_regular_user():
    return User(username="regular", is_admin=False)

def test_regular_user_forbidden():
    app.dependency_overrides[get_current_user] = override_get_regular_user
    app.dependency_overrides.pop(get_current_active_admin_user, None)
    response = client.get("/config/platforms")
    assert response.status_code == 403

def test_admin_user_allowed():
    app.dependency_overrides[get_current_user] = override_get_admin_user
    app.dependency_overrides.pop(get_current_active_admin_user, None)

    # We don't want the actual db execution to fail
    from backend.database import get_db
    from unittest.mock import AsyncMock
    async def override_get_db():
        db = AsyncMock()
        db.execute = AsyncMock(return_value=AsyncMock(scalars=lambda: AsyncMock(all=lambda: [])))
        yield db

    app.dependency_overrides[get_db] = override_get_db

    response = client.get("/config/platforms")
    assert response.status_code == 200
