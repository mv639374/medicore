# What & Why: A set of unit tests to verify that our security functions work exactly as expected. Testing security code is non-negotiable to ensure there are no vulnerabilities.

import pytest

from backend.app.core.permissions import Permission, UserRole, check_permission
from backend.app.core.security import (
    create_access_token,
    decode_token,
    get_password_hash,
    verify_password,
)


def test_password_hashing():
    password = "strongpassword123"
    haseded_password = get_password_hash(password)
    assert haseded_password != password
    assert verify_password(password, hashed_password=haseded_password)
    assert not verify_password("wrongpassword", haseded_password)


def test_jwt_token_creation_and_decoding():
    user_data = {"sub": "test@example.com", "role": "admin"}
    token = create_access_token(data=user_data)
    decoded_payload = decode_token(token)
    assert decoded_payload["sub"] == user_data["sub"]
    assert decoded_payload["role"] == user_data["role"]


def test_permission_checking():
    assert check_permission(UserRole.ADMIN, Permission.MANAGE_USERS)
    assert check_permission(UserRole.DOCTOR, Permission.READ_DIAGNOSITICS)
    assert not check_permission(UserRole.TECHNICIAN, Permission.MANAGE_USERS)
