"""
Unit tests for the example protected and public routes.
"""
from fastapi.testclient import TestClient

# --- Helper to get a valid token ---
def get_jwt_token(client: TestClient) -> str:
    """Utility function to get a valid JWT token for tests."""
    response = client.post(
        "/login/token",
        data={"username": "testuser", "password": "testpassword"},
    )
    return response.json()["access_token"]


# --- Tests for the public endpoint ---
def test_unprotected_route(client: TestClient):
    """Test that the public route is accessible without authentication."""
    response = client.get("/examples/public/unprotected")
    assert response.status_code == 200
    assert response.json()["message"] == "This endpoint is public and requires no authentication."


# --- Tests for the JWT-only endpoint ---
def test_jwt_only_route_success(client: TestClient):
    """Test successful access to JWT-only route with a valid token."""
    token = get_jwt_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/examples/protected/jwt-only", headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Hello testuser, you are authenticated via JWT."


def test_jwt_only_route_no_token(client: TestClient):
    """Test access failure to JWT-only route without a token."""
    response = client.get("/examples/protected/jwt-only")
    assert response.status_code == 401


# --- Tests for the simple token endpoint ---
def test_simple_token_route_success(client: TestClient):
    """Test successful access to simple token route with a valid token."""
    # This token comes from the overridden test settings
    headers = {"Authentication": "test-static-api-token"}
    response = client.get(
        "/examples/protected/simple-token-only", headers=headers
    )
    assert response.status_code == 200
    assert response.json()["message"] == "You are authenticated via a simple API token."


def test_simple_token_route_wrong_token(client: TestClient):
    """Test access failure to simple token route with a wrong token."""
    headers = {"Authentication": "wrong-token"}
    response = client.get(
        "/examples/protected/simple-token-only", headers=headers
    )
    assert response.status_code == 401


# # --- Tests for the dual-authentication endpoint ---
# def test_any_auth_route_with_jwt(client: TestClient):
#     """Test successful access to 'any-auth' route using JWT."""
#     token = get_jwt_token(client)
#     headers = {"Authorization": f"Bearer {token}"}
#     response = client.get("/examples/protected/any-auth", headers=headers)
#     assert response.status_code == 200
#     # assert response.json()["auth_method"] == "jwt"


# def test_any_auth_route_with_simple_token(client: TestClient):
#     """Test successful access to 'any-auth' route using the simple token."""
#     headers = {"Authentication": "test-static-api-token"}
#     response = client.get("/examples/protected/any-auth", headers=headers)
#     assert response.status_code == 200
#     assert response.json()["auth_method"] == "simple_token"


# def test_any_auth_route_no_token(client: TestClient):
#     """Test access failure to 'any-auth' route with no token."""
#     response = client.get("/examples/protected/any-auth")
#     assert response.status_code == 401
