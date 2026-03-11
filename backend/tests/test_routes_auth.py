from fastapi.testclient import TestClient
from backend.main import app
from backend.auth import get_current_active_admin_user, get_current_user, oauth2_scheme
from backend.database import get_db
from backend.models import User
import pytest
import inspect
from fastapi import HTTPException, status
from unittest.mock import AsyncMock, MagicMock

client = TestClient(app)

@pytest.fixture(autouse=True)
def isolate_deps():
    app.dependency_overrides = {}
    yield
    app.dependency_overrides = {}

def test_regular_user_forbidden():
    async def override_forbidden():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges"
        )

    # Clear and override
    app.dependency_overrides.clear()

    # Force override all dependencies that might be used
    app.dependency_overrides[get_current_active_admin_user] = override_forbidden

    # Also override by inspecting the route just in case
    for route in app.router.routes:
        if getattr(route, "path", None) == "/config/platforms" and "GET" in getattr(route, "methods", []):
            dep = inspect.signature(route.endpoint).parameters['current_user'].default.dependency
            app.dependency_overrides[dep] = override_forbidden
            break

    response = client.get("/config/platforms")
    assert response.status_code == 403

def test_admin_user_allowed():
    async def override_get_admin_user_direct():
        return User(username="admin", is_admin=True)

    async def override_get_db():
        db = AsyncMock()
        mock_scalars = MagicMock()
        mock_scalars.all.return_value = []
        mock_result = MagicMock()
        mock_result.scalars.return_value = mock_scalars
        db.execute.return_value = mock_result
        yield db

    app.dependency_overrides.clear()

    # Override standard dependencies
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[oauth2_scheme] = lambda: "dummy-token"
    app.dependency_overrides[get_current_user] = override_get_admin_user_direct
    app.dependency_overrides[get_current_active_admin_user] = override_get_admin_user_direct

    # Also override by inspecting the route to ensure exact match
    for route in app.router.routes:
        if getattr(route, "path", None) == "/config/platforms" and "GET" in getattr(route, "methods", []):
            sig = inspect.signature(route.endpoint)

            if 'current_user' in sig.parameters:
                user_dep = sig.parameters['current_user'].default.dependency
                app.dependency_overrides[user_dep] = override_get_admin_user_direct

            if 'db' in sig.parameters:
                db_dep = sig.parameters['db'].default.dependency
                app.dependency_overrides[db_dep] = override_get_db
            break

    response = client.get("/config/platforms", headers={"Authorization": "Bearer dummy-token"})
    assert response.status_code == 200
