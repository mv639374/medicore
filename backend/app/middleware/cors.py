# What: This configures CORS (Cross-Origin Resource Sharing). It's a security feature that browsers use to restrict which websites can make requests to your API.
# Why: Our frontend (running on localhost:3000) and backend (on localhost:8000) are considered different "origins." This middleware tells the browser that it's okay for our frontend to talk to our backend.

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from backend.app.config import settings

def configure_cors(app: FastAPI):
    """
    Configures CORS middleware for the FastAPI application.
    Origins for production should be loaded from settings.
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.CORS_ORIGINS],
        allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
        allow_methods=["*"], # Allow all methods
        allow_headers=["*"], # Allow all headers
    )
