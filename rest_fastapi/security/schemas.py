"""
Pydantic models for security and authentication.

This module defines the data structures used in the authentication
process, such as the format of the JWT token data and the response
model for a successful token request.
"""
from pydantic import BaseModel
from typing import Optional


class TokenData(BaseModel):
    """
    Data model for the contents of a JWT.

    Attributes
    ----------
    username : str or None
        The subject of the token, typically the user's username.
    """
    username: Optional[str] = None


class Token(BaseModel):
    """
    Response model for a successful authentication request.

    Attributes
    ----------
    access_token : str
        The JWT access token.
    token_type : str
        The type of the token (e.g., "bearer").
    """
    access_token: str
    token_type: str
