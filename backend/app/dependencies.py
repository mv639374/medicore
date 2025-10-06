# What: This file will hold our dependency injection functions. These are special functions that FastAPI can run before processing a request. For now, we are creating placeholders for getting the current user and checking their permissions.
# Why: Dependencies help us write reusable logic (like authentication checks) and keep our endpoint code clean and focused. Instead of writing user-checking code in every endpoint, we can just "depend" on get_current_user.

from fastapi import Depends

from backend.app.core.exceptions import ForbiddenException, UnauthorizedException
from backend.app.core.permissions import Permission, check_permission
from backend.app.middleware.auth import JWTBearer
from backend.app.models.database.user import User, UserRole


# Dependency to get the current user from the JWT token
async def get_current_user(payload: dict = Depends(JWTBearer())) -> User:
    # In a real app, you'd query the DB here based on payload['sub]
    # For now, we'll mock a user object.
    # user = db.query(User).filter(User.email == payload['sub']).first()
    # if not user: raise UnauthorizedException()
    mock_user = User(
        email=payload.get("sub"),
        role=UserRole(payload.get("role", "viewer")),
        is_active=True,
    )
    return mock_user


# Dependency to get a current user who is also active
def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise UnauthorizedException("Inactive user")
    return current_user


# Dependency factory for requiring a specific permission
def require_permission(permission: Permission):
    def permission_checker(current_user: User = Depends(get_current_active_user)):
        if not check_permission(current_user.role, permission):
            raise ForbiddenException("You do not have the required permission.")
        return current_user

    return permission_checker
