# What: An orchestrator service that handles the end-to-end logic for a DICOM upload. It saves the file, creates a database record, and then triggers the background Celery task.

# Why: This service connects our API endpoint to the database and the async task queue. It provides a single, clean entry point for the entire DICOM processing workflow.

import logging
import tempfile
import uuid
from pathlib import Path
from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.core.utils import generate_unique_filename, format_dicom_date
from app.services.dicom.parser import parse_dicom_file, get_dicom_metadata
from app.services.dicom.validator import validate_dicom_standard
from app.services.storage.s3_client import S3Client
from app.models.database.study import DICOMStudy
from app.workers.tasks.diagnostic import process_dicom_async
from app.config import settings

logger = logging.getLogger(__name__)

class DICOMProcessor:
    def __init__(self, db: Session):
        self.db = db
        self.s3_client = S3Client()

    async def process_upload(self, file: UploadFile, patient_id: uuid.UUID) -> dict:
        """
        Processes an uploaded DICOM file, saves it, creates a DB record,
        and triggers an async processing task.
        """
        # Save upload to a temporary file
        temp_dir = Path(settings.DICOM_TEMP_DIR)
        temp_dir.mkdir(parents=True, exist_ok=True)
        temp_file_path = temp_dir / generate_unique_filename(file.filename)
        
        with open(temp_file_path, "wb") as buffer:
            buffer.write(await file.read())

        try:
            # Basic parsing and validation before creating the record
            dicom_dataset = parse_dicom_file(str(temp_file_path))
            is_valid, errors = validate_dicom_standard(dicom_dataset)
            if not is_valid:
                raise ValueError(f"Invalid DICOM file: {', '.join(errors)}")
            
            metadata = get_dicom_metadata(dicom_dataset)

            # Upload original file to S3
            s3_key = f"studies/{metadata['StudyInstanceUID']}/{temp_file_path.name}"
            upload_success = self.s3_client.upload_file(str(temp_file_path), s3_key)
            if not upload_success:
                raise IOError("Failed to upload file to S3.")

            # Create the database record
            new_study = DICOMStudy(
                patient_id=patient_id,
                study_instance_uid=metadata['StudyInstanceUID'],
                series_instance_uid=metadata['SeriesInstanceUID'],
                sop_instance_uid=metadata['SOPInstanceUID'],
                modality=metadata['Modality'],
                study_date=format_dicom_date(metadata['StudyDate']),
                study_description=metadata['StudyDescription'],
                s3_bucket=self.s3_client.bucket_name,
                s3_key=s3_key,
                processing_status="pending"
            )
            self.db.add(new_study)
            self.db.commit()
            self.db.refresh(new_study)

            # Trigger the async task
            task = process_dicom_async.delay(str(new_study.id))

            return {"study_id": new_study.id, "task_id": task.id, "status": "processing_started"}

        finally:
            # Clean up the temporary file
            if temp_file_path.exists():
                temp_file_path.unlink()