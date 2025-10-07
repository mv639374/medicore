# What: A new SQLAlchemy model that represents a DICOMStudy in our database.
# Why: This is how we store the metadata of every DICOM file we process. Storing metadata in the database allows us to quickly search and filter studies (e.g., "find all CT scans for patient X") without having to download and read every file from S3.

# Update: Why: Adding new columns to our DICOMStudy model to track the status (pending, completed, failed) and results of our asynchronous processing.

import uuid
from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base

class DICOMStudy(Base):
    __tablename__ = "dicom_studies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.id"), nullable=False, index=True)
    
    study_instance_uid = Column(String(255), unique=True, nullable=False, index=True)
    series_instance_uid = Column(String(255), nullable=False, index=True)
    sop_instance_uid = Column(String(255), nullable=False, unique=True)
    
    modality = Column(String(10), nullable=False, index=True)
    study_date = Column(Date, nullable=True)
    study_time = Column(String(20), nullable=True)
    study_description = Column(Text, nullable=True)
    institution_name = Column(String(255), nullable=True)
    manufacturer = Column(String(255), nullable=True)
    
    s3_bucket = Column(String(255), nullable=False)
    s3_key = Column(String(500), nullable=False)

    # New columns for processing status
    processing_status = Column(String(20), default="pending", index=True, nullable=False)
    processing_error = Column(Text, nullable=True)
    processed_at = Column(DateTime, nullable=True)
    quality_metrics = Column(JSON, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    patient = relationship("Patient", back_populates="studies")
    # diagnostic = relationship("DiagnosticResult", back_populates="study") # To be added in a later phase