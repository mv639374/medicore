# Defines the User data model.
# What: This class maps to a users table. It includes fields for email, a hashed password, user role, and status flags.
# Why: The UserRole enum provides a clear, controlled set of roles for implementing role-based access control (RBAC). Storing a hashed_password instead of the plain text password is a critical security practice.

import enum
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Enum, Integer, String, func

from backend.app.database import Base


class UserRole(enum.Enum):
    ADMIN = "admin"
    DOCTOR = "doctor"
    RADIOLOGIST = "radiologist"
    TECHNICIAN = "technician"
    VIEWER = "viewer"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.VIEWER)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # columns for security
    failed_login_attemps = Column(Integer, default=0)
    account_locked_until = Column(DateTime, nullable=True)

    def is_account_locked(self) -> bool:
        """Checks if the account is currently locked."""
        return (
            self.account_locked_until is not None
            and self.account_locked_until > datetime.utcnow()
        )
