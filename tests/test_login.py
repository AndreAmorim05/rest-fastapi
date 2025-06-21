"""
Unit tests for the login and token generation endpoint.
"""
from fastapi.testclient import TestClient


def test_login_for_access_token_success(client: TestClient):
    """
    Test successful authentication and token generation.
    """
    response = client.post(
        "/login/token",
        data={"username": "testuser", "password": "testpassword"},
    )
    json_response = response.json()

    assert response.status_code == 200
    assert "access_token" in json_response
    assert json_response["token_type"] == "bearer"


def test_login_for_access_token_wrong_password(client: TestClient):
    """
    Test authentication failure with an incorrect password.
    """
    response = client.post(
        "/login/token",
        data={"username": "testuser", "password": "wrongpassword"},
    )
    json_response = response.json()

    assert response.status_code == 401
    assert json_response["detail"] == "Incorrect username or password"


def test_login_for_access_token_wrong_username(client: TestClient):
    """
    Test authentication failure with a non-existent username.
    """
    response = client.post(
        "/login/token",
        data={"username": "wronguser", "password": "testpassword"},
    )
    json_response = response.json()

    assert response.status_code == 401
    assert json_response["detail"] == "Incorrect username or password"
