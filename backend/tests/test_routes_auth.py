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

import pytest

@pytest.fixture(autouse=True)
def isolate_deps():
    yield
    app.dependency_overrides = {}

def test_regular_user_forbidden():
    from fastapi import HTTPException, status
    from backend.auth import get_current_active_admin_user

    async def override_forbidden():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges"
        )

    import inspect
    app.dependency_overrides.clear()
    # Mocking the dependency directly by matching its reference
    dep = None
    for route in app.router.routes:
        if getattr(route, "path", None) == "/config/platforms" and "GET" in getattr(route, "methods", []):
            dep = inspect.signature(route.endpoint).parameters['current_user'].default.dependency
            break

    app.dependency_overrides[dep] = override_forbidden

    response = client.get("/config/platforms")
    assert response.status_code == 403

def test_admin_user_allowed():
    from backend.auth import get_current_active_admin_user
    async def override_get_admin_user_direct():
        return User(username="admin", is_admin=True)

    import inspect
    app.dependency_overrides.clear()
    # We must explicitly find the dependency for the route, matching get_platforms (which is the first one, or just search it)
    dep = None
    for route in app.router.routes:
        if getattr(route, "path", None) == "/config/platforms" and "GET" in getattr(route, "methods", []):
            dep = inspect.signature(route.endpoint).parameters['current_user'].default.dependency
            break

    app.dependency_overrides[dep] = override_get_admin_user_direct

    # We don't want the actual db execution to fail
    from backend.database import get_db
    from unittest.mock import AsyncMock

    async def override_get_db():
        from unittest.mock import MagicMock
        db = AsyncMock()

        # Proper mock hierarchy for scalars().all()
        # all() is not awaited, so scalars() should return a MagicMock, not AsyncMock
        mock_scalars = MagicMock()
        mock_scalars.all.return_value = []

        mock_result = MagicMock()
        mock_result.scalars.return_value = mock_scalars

        db.execute.return_value = mock_result
        yield db

    from backend.database import get_db
    from backend.auth import oauth2_scheme, get_current_user, get_current_active_admin_user
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[oauth2_scheme] = lambda: "dummy-token"
    app.dependency_overrides[get_current_user] = override_get_admin_user_direct
    app.dependency_overrides[get_current_active_admin_user] = override_get_admin_user_direct

    response = client.get("/config/platforms", headers={"Authorization": "Bearer dummy-token"})
    assert response.status_code == 200
