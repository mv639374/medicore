# Defines the AuditLog model for tracking user actions.
# What: This model maps to an audit_logs table. It records who did what, to what resource, and when.
# Why: This is essential for security and HIPAA compliance. It gives us a trail of all significant actions performed in the system, which is crucial for security audits and for investigating any potential data breaches.

from datetime import datetime
from ipaddress import ip_address
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from backend.app.database import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True) # Nullable for system actions
    action = Column(String(100), nullable=False, index=True)
    resource = Column(String(100), nullable=False, index=True)
    resource_id = Column(String(100), nullable=True)
    details = Column(Text, nullable=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(255), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True, nullable=False)

    def __repr__(self):
        return f"<Auditlog(id={self.id}, action='{self.action}')>"