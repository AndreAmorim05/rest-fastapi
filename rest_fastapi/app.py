"""
Main application factory.

This module contains the `create_app` factory function, which
initializes and configures the FastAPI application instance.
"""
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from rest_fastapi.routes.api import init_api_routes


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    This function initializes the application, sets up CORS middleware,
    and calls the route initializer to include all API routes.

    Returns
    -------
    FastAPI
        The configured FastAPI application instance.
    """
    app = FastAPI(
        title="Multi-Auth API (Resource Pattern)",
        description="An API with JWT and Simple Token authentication "
        "using class-based resources.",
        version="2.0.0",
    )

    # Configure CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Initialize all API routes from a central function
    init_api_routes(app)

    return app
