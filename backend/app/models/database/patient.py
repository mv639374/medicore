# This file defines the Patient data model.
# What: It's a Python class that maps to the patients table in our database. The columns (id, encrypted_name, etc.) correspond to the fields in that table.
# Why: We use LargeBinary for sensitive patient data because we will encrypt this data before storing it, and the encrypted result is binary. This is a key part of our HIPAA compliance strategy. The UUID primary key is used to avoid exposing sequential integer IDs.

import uuid
from datetime import datetime
from sqlalchemy import Column, DateTime, LargeBinary, String
from sqlalchemy.dialects.postgresql import UUID
from backend.app.database import Base

class Patient(Base):
    __tablename__ = "patients"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    encrypted_name = Column(LargeBinary, nullable=False)
    encrypted_dob = Column(LargeBinary, nullable=False)
    encrypted_ssn = Column(LargeBinary, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<Patient(id='{self.id}')>"

# Note: The actual encryption/decryption logic will be added later in the security module.