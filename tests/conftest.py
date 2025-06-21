"""
Configuration and fixtures for the Pytest test suite.

This file provides shared fixtures, most importantly the FastAPI
TestClient, which is configured to override the application's settings
dependency. This ensures that all tests run with a predictable,
isolated configuration, independent of any real .env files.
"""
import pytest
from fastapi.testclient import TestClient

from rest_fastapi.app import create_app
from rest_fastapi.core.config import Settings, get_settings


def get_test_settings() -> Settings:
    """
    Return a Settings object with predictable test values.

    This function overrides the production 'get_settings' dependency,
    allowing tests to run in a completely isolated environment.
    """
    return Settings(
        ENV_STATE="dev",
        SECRET_KEY="test-secret-key-for-jwt-dont-use-in-prod",
        ALGORITHM="HS256",
        ACCESS_TOKEN_EXPIRE_SECONDS=15*60,
        SIMPLE_API_TOKEN="test-static-api-token",
        USER_LOGIN={"testuser": {"password": "testpassword"}}
    )


@pytest.fixture(scope="module")
def client() -> TestClient:
    """
    Pytest fixture to create a FastAPI TestClient.

    This client is used to make requests to the application within
    tests. It's configured with the dependency override for settings.
    """
    # Create the app instance
    app = create_app()

    # Override the settings dependency for the entire application
    app.dependency_overrides[get_settings] = get_test_settings

    # Yield a TestClient for making requests
    with TestClient(app) as test_client:
        yield test_client
