# What: A custom middleware that logs details about every single request that comes into our API and the response that goes out.
# Why: This is crucial for debugging and monitoring. It tells us which endpoints are being used, how long they take to process, and what the outcome was (e.g., success 200 OK or an error 500).

import time
import logging
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

# Configure a basic logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        # Process the request
        response = await call_next(request)

        # Calculate processing time
        process_time = time.time() - start_time

        # Log request and response details
        logger.info(
            f"Request: {request.method} {request.url.path} - "
            f"Response: {response.status_code} - "
            f"Duration: {process_time:.4f}s"
        )
        return response

