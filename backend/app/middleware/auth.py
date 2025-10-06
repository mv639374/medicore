# What: This is the actual JWT authentication middleware. It inherits from HTTPBearer, which knows how to look for the Authorization: Bearer <token> header.
# Why: This middleware will run on protected requests. It automatically extracts the token, uses our decode_token function to validate it, and attaches the user's data to the request for later use. If the token is invalid, it stops the request and returns an UnauthorizedException.

from typing import Optional

from fastapi import Request
from fastapi.security import HTTPBearer

from backend.app.core.exceptions import UnauthorizedException
from backend.app.core.security import decode_token


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise UnauthorizedException("Invalid authentication scheme.")

            payload = decode_token(credentials.credentials)

            if payload is None:
                raise UnauthorizedException("Invalid or expired token.")

            request.state.user = payload
            return payload
        else:
            raise UnauthorizedException("Authentication token required.")
