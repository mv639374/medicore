# What: This file defines our Role-Based Access Control (RBAC) system. It lists specific Permissions and maps them to each UserRole.

# Why: RBAC ensures that users can only perform actions they are authorized to do. For example, a TECHNICIAN can upload a diagnostic but cannot MANAGE_USERS. This is a fundamental security principle.

from enum import Enum

from app.models.database.user import UserRole


class Permission(Enum):
    READ_DIAGNOSTICS = "read_diagnostics"
    CREATE_DIAGNOSTICS = "create_diagnostics"
    UPDATE_DIAGNOSTICS = "update_diagnostics"
    DELETE_DIAGNOSTICS = "delete_diagnostics"
    MANAGE_USERS = "manage_users"
    VIEW_ANALYTICS = "view_analytics"
    EXPORT_DATA = "export_data"


# Mapping roles to their allowed permissions
role_permissions = {
    UserRole.ADMIN: [p for p in Permission],  # Admin has all permissions
    UserRole.DOCTOR: [
        Permission.READ_DIAGNOSTICS,
        Permission.CREATE_DIAGNOSTICS,
        Permission.UPDATE_DIAGNOSTICS,
        Permission.VIEW_ANALYTICS,
    ],
    UserRole.RADIOLOGIST: [
        Permission.READ_DIAGNOSTICS,
        Permission.CREATE_DIAGNOSTICS,
        Permission.UPDATE_DIAGNOSTICS,
    ],
    UserRole.TECHNICIAN: [
        Permission.CREATE_DIAGNOSTICS,
    ],
    UserRole.VIEWER: [Permission.READ_DIAGNOSTICS],
}


def check_permission(user_role: UserRole, required_permission: Permission) -> bool:
    """Checks if a user role has a specific permission."""
    return required_permission in role_permissions.get(user_role, [])
