# What: This is the heart of our authentication system. It contains functions for hashing and verifying passwords, and for creating and decoding JWTs.

# Why: We never store passwords directly. We store a hash. This file uses bcrypt, a strong hashing algorithm. JWTs are used to securely transmit user information between the client and server after they log in.

from datetime import datetime, timedelta
from typing import Dict, Optional

from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import deprecated

from backend.app.config import settings

# Setup for password hashing using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain password against a hashed one."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hashes a plain password."""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Creates a new JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRATION_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


def decode_token(token: str) -> Optional[Dict]:
    """Decodes a JWT token, returning the payload if valid."""
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except JWTError:
        return None
