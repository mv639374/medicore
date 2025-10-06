# What: This middleware protects our API from being overwhelmed by too many requests from a single IP address.
# Why: This is a crucial defense against brute-force attacks (e.g., someone trying to guess a password thousands of times) and Denial-of-Service (DoS) attacks.

from fastapi import FastAPI
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from backend.app.config import settings

limiter = Limiter(key_func=get_remote_address, enabled=settings.RATE_LIMIT_ENABLED)


def configure_rate_limiting(app: FastAPI):
    """Adds the rate limiter to the application."""
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
