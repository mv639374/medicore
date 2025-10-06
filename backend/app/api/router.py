# What: This file creates the main API router. A router is like a mini-FastAPI application that can group related endpoints.
# Why: As our application grows, we'll have many endpoints (for users, patients, diagnostics, etc.). This main router acts as the entry point, and we will attach all the other specific routers to it. This keeps our code organized.

from fastapi import APIRouter

# Create the main API router with a prefix for versioning
api_router = APIRouter(prefix="/api/v1")


@api_router.get("/info")
def get_api_info():
    """Returns basic information about the API."""
    return {
        "status": "ok",
        "api_version": "1.0.0",
        "message": "Welcome to the MediCore API!",
    }


# Placeholder comments for future endpoint routers
# from .v1.endpoints import auth
# api_router.include_router(auth.router, perfix="/auth", tags=["Authentication"])

# from .v1.endpoints import patients
# api_router.include_router(patients.router, perfix="/patients", tags=["Patients"])
