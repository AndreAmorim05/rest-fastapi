"""
Unit tests for security logic, such as token expiration.
"""
import time
from datetime import timedelta

from fastapi.testclient import TestClient
from freezegun import freeze_time

from rest_fastapi.app import create_app
from rest_fastapi.core.config import get_settings, Settings


def test_token_expiration(client: TestClient):
    """
    Test that a JWT token correctly expires after its lifetime.
    """
    # --- Part 1: Create a token with a very short lifetime ---

    # Define test-specific settings with a 1-second expiration
    def get_short_lived_token_settings():
        return Settings(
            ENV_STATE="dev",
            SECRET_KEY="test-secret",
            ACCESS_TOKEN_EXPIRE_SECONDS=1/60,  # 1 second
            SIMPLE_API_TOKEN="test-api-token",
        )

    # Override the dependency just for this test's scope
    client.app.dependency_overrides[get_settings] = get_short_lived_token_settings

    # Get the short-lived token
    response = client.post(
        "/login/token",
        data={"username": "testuser", "password": "testpassword"},
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # --- Part 2: Use the token immediately, it should be valid ---
    response_before_expiry = client.get(
        "/examples/protected/jwt-only", headers=headers
    )
    assert response_before_expiry.status_code == 200
    assert response_before_expiry.json()["message"] == "Hello testuser, you are authenticated via JWT."

    # --- Part 3: Wait for more than 1 second and try again ---
    time.sleep(2)

    response_after_expiry = client.get(
        "/examples/protected/jwt-only", headers=headers
    )
    assert response_after_expiry.status_code == 401
    assert response_after_expiry.json()["detail"] == "Could not validate JWT credentials"

    # --- Part 4: Clean up the dependency override ---
    # This is important to not affect other tests
    client.app.dependency_overrides = {}
