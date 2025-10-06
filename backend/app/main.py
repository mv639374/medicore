import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from backend.app.api.router import api_router
from backend.app.config import settings
from backend.app.core.exceptions import (
    BadRequestException,
    ForbiddenException,
    NotFoundException,
    UnauthorizedException,
)
from backend.app.middleware.cors import configure_cors
from backend.app.middleware.logging import LoggingMiddleware
from backend.app.middleware.rate_limiting import configure_rate_limiting, limiter

app = FastAPI(
    title="Medicore API",
    version="1.0.0",
    description="AI-Powered Healthcare Diagnostic Platform API",
    openapi_url=settings.OPENAPI_URL,
)

logger = logging.getLogger(__name__)

# --- Middleware ---

configure_rate_limiting(app)
# Note: Middleware is processed in the reverse order it's added.
configure_cors(app)
# LoggingMiddleware will wrap everything.
app.add_middleware(LoggingMiddleware)


# Middleware to add security headers
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Strict-Transport-Security"] = (
        "max-age=31536000; includeSubDomains"
    )
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response


# --- Exception Handlers ---
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    # In production, you would want to log this exception.
    return JSONResponse(
        status_code=500, content={"detail": "An unexpected server error occurred."}
    )


# --- Events ---
@app.on_event("startup")
async def startup_event():
    logger.info("Medicore API starting...")
    # Here you could add a database connection test if desired.


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("MediCore API shutting down...")


# --- Routers ---
@app.get("/")
def read_root():
    """Root endpoint for the API"""
    return {"status": "ok", "message": "Medicore API is running"}


@app.get("/health")
@limiter.limit("100/minute")
async def health_check(request: Request):
    """Health Check endpoint for monitoring."""
    return {"status": "healthy", "version": "1.0.0"}


# Include the main API router
app.include_router(api_router)

# Will come back to this file later to add middleware, routes, etc.
