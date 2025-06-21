"""
API route initialization.

This module centralizes the registration of all API routes and their
corresponding class-based controllers (resources).
"""
from fastapi import FastAPI

from rest_fastapi.controllers import login, protected


def init_api_routes(app: FastAPI):
    """
    Include all API routers in the FastAPI application.

    This function takes the main app instance and includes the routers
    defined in the controller modules. This adheres to the pattern of
    centralized route registration.

    Parameters
    ----------
    app : FastAPI
        The main FastAPI application instance.
    """
    app.include_router(login.router)
    app.include_router(protected.router)
