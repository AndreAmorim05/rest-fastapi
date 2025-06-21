"""
Authentication dependencies for FastAPI.

This module provides reusable dependency functions for route protection.
This approach is idiomatic for FastAPI and ensures that security schemes
are correctly registered in the OpenAPI specification, making the
'Authorize' button functional in the /docs UI.
"""

from datetime import datetime, timedelta, timezone
from typing import Annotated, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, APIKeyHeader
from jose import JWTError, jwt

from rest_fastapi.core.config import Settings, get_settings
from rest_fastapi.security.schemas import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")
api_key_header_scheme = APIKeyHeader(name="Authentication")


def create_access_token(
    data: dict, settings: Settings, expires_delta: Optional[timedelta] = None
) -> str:
    """Create a new JWT access token.

    Parameters
    ----------
    data : dict
        The data payload to include in the token (e.g., 'sub' for subject).
    settings : Settings
        The application settings, injected via dependency.
    expires_delta : Optional[timedelta], optional
        The specific lifespan for this token. If not provided, it defaults
        to the value from the application settings. The default is None.

    Returns
    -------
    str
        The encoded JWT access token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


# --- Authentication Dependency Functions ---

def auth_jwt(
    token: Annotated[str, Depends(oauth2_scheme)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> TokenData:
    """Dependency for routes requiring JWT authentication."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate JWT credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: Optional[str] = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    return token_data


def auth_token(
    token: Annotated[str, Depends(api_key_header_scheme)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> str:
    """Dependency for routes requiring a simple static API token."""
    if token != settings.SIMPLE_API_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API token",
        )
    return token


# def auth_general(
#     # By depending on the schemes and marking them Optional with a default
#     # of None, FastAPI registers them for the docs but passes `None` if
#     # they are missing, instead of raising an error.
#     token: Annotated[Optional[str], Depends(oauth2_scheme)] = None,
#     api_key: Annotated[Optional[str], Depends(api_key_header_scheme)] = None,
#     settings: Annotated[Settings, Depends(get_settings)] = None,
# ) -> dict:
#     """Dependency for routes allowing either JWT or simple token auth."""
#     # This dependency can't function without settings.
#     if not settings:
#         settings = get_settings()

#     if token:
#         try:
#             payload = jwt.decode(
#                 token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
#             )
#             username: Optional[str] = payload.get("sub")
#             if username:
#                 return {
#                     "user": TokenData(username=username),
#                     "method": "jwt"
#                 }
#         except JWTError:
#             pass  # Invalid JWT, fall through to check API key.

#     if api_key:
#         if api_key == settings.SIMPLE_API_TOKEN:
#             return {"user": None, "method": "simple_token"}
#         else:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Invalid API Key provided."
#             )

#     raise HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Not authenticated. Provide a valid Bearer or API token.",
#         headers={"WWW-Authenticate": "Bearer, APIKey"},
#     )
