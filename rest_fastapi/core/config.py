"""
Module for application configuration management.

This module uses Pydantic's BaseSettings for type-safe configuration
management. It includes logic to dynamically locate the .env file in
predefined production or local development paths, providing both
flexibility and robustness.
"""
import os
import pathlib
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

# --- Helper function to find the .env file ---

def find_env_file() -> str | None:
    """
    Find the .env file in predefined locations.

    It first checks for a global secrets file (common in containerized
    environments) and then falls back to a local file for development.

    Returns
    -------
    str or None
        The path to the found .env file, or None if not found.
    """
    # 1. Path for production/containerized environment
    prod_env_path = "/secrets/.env"
    if os.path.exists(prod_env_path):
        return prod_env_path

    # 2. Path for local development
    # BASE_DIR should point to the project root, where 'secrets' lives
    base_dir = pathlib.Path(__file__).resolve().parent.parent.parent
    local_env_path = base_dir / "secrets" / ".env"
    if os.path.exists(local_env_path):
        return str(local_env_path)

    # 3. Fallback if no file is found
    print("WARNING: .env file not found in specified paths.")
    return None

# --- Pydantic Settings Class ---

class Settings(BaseSettings):
    """
    Application settings, validated by Pydantic.

    Attributes are automatically loaded from environment variables or a
    .env file. Pydantic ensures that the variables have the correct
    type, raising an error on startup if they are missing or invalid.

    Attributes
    ----------
    ENV_STATE : Literal["dev", "prod"]
        The application environment state.
    SECRET_KEY : str
        The secret key for signing JWTs.
    ALGORITHM : str
        The algorithm to use for signing JWTs.
    ACCESS_TOKEN_EXPIRE_MINUTES : int
        The lifetime of an access token in minutes.
    SIMPLE_API_TOKEN : str
        A simple, static token for basic API authentication.
    """
    # --- Project Specific ---
    ENV_STATE: Literal["dev", "prod"] = "dev"

    # --- JWT Authentication ---
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_SECONDS: float = 30 * 60  # Default to 30 minutes

    # --- Simple Token Authentication ---
    SIMPLE_API_TOKEN: str

    # --- Optional: Database settings can be added here if needed ---
    USER_LOGIN: dict

    # Pydantic model configuration
    model_config = SettingsConfigDict(
        env_file=find_env_file(),  # Dynamically find the .env file
        env_file_encoding='utf-8',
        extra='ignore'  # Ignore extra variables in the .env file
    )


# --- Instantiate settings ---
# This single instance will be imported by other parts of the application.
settings = Settings()


def get_settings() -> Settings:
    """
    Dependency function to get the application settings.

    Returns
    -------
    Settings
        The application settings instance.
    """
    return settings
