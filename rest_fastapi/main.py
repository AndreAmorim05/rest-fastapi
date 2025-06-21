"""
Main entry point for the application.

This script creates the FastAPI app instance using the factory and
is used by Uvicorn to run the server.
"""
import uvicorn
from rest_fastapi.app import create_app

app = create_app()

if __name__ == "__main__":
    # To run this application:
    # uvicorn main:app --reload
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
