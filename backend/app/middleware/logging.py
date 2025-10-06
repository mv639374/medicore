# What: A custom middleware that logs details about every single request that comes into our API and the response that goes out.
# Why: This is crucial for debugging and monitoring. It tells us which endpoints are being used, how long they take to process, and what the outcome was (e.g., success 200 OK or an error 500).
# Update: Why: We're upgrading to structured logging. Adding a unique request_id to every log entry makes it much easier to trace a single request's journey through our system, which is invaluable for debugging.

import logging
import time
import uuid

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

# Configure a basic logger
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# class LoggingMiddleware(BaseHTTPMiddleware):
#     async def dispatch(self, request: Request, call_next):
#         start_time = time.time()

#         # Process the request
#         response = await call_next(request)

#         # Calculate processing time
#         process_time = time.time() - start_time

#         # Log request and response details
#         logger.info(
#             f"Request: {request.method} {request.url.path} - "
#             f"Response: {response.status_code} - "
#             f"Duration: {process_time:.4f}s"
#         )
#         return response


class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        """The main logic of the middleware."""

        request_id = str(uuid.uuid4())
        request.state.request_id = request_id

        start_time = time.time()

        # This is where the request is passed to the next middleware or endpoint
        response = await call_next(request)

        # Calculate processing time
        process_time = (time.time() - start_time) * 1000

        log_message = (
            f"rid={request_id} "
            f"method={request.method} "
            f"path={request.url.path} "
            f"status={response.status_code} "
            f"duration_ms={process_time:.2f} "
        )

        # Log request and response details
        logger.info(log_message)
        return response
