# What & Why: These are Pydantic models (schemas) used by FastAPI to define the shape of our API's input and output for study-related data. They ensure data validation and provide clear documentation.

from pydantic import BaseModel, UUID4
from typing import Optional
from datetime import date, datetime

class StudyResponse(BaseModel):
    id: UUID4
    patient_id: UUID4
    study_instance_uid: str
    modality: str
    study_date: Optional[date]
    s3_key: str
    created_at: datetime

    class Config:
        orm_mode = True

class StudyUploadResponse(BaseModel):
    study_id: UUID4
    status: str
    message: str