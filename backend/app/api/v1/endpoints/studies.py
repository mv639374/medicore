# What: The API endpoints for managing studies. For now, we are creating a placeholder for the /upload endpoint.
# Why: This provides the HTTP interface for our frontend to interact with the DICOM processing pipeline.

from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from pydantic import UUID4
from sqlalchemy.orm import Session

from app.dependencies import get_current_active_user, get_db
from app.services.dicom.processor import DICOMProcessor
from app.workers.celery_app import celery_app

# We will implement the processor and schemas later
# from backend.app.services.dicom.processor import DICOMProcessor 
# from backend.app.models.schemas.study import StudyUploadResponse

router = APIRouter()

@router.post("/upload", status_code=status.HTTP_202_ACCEPTED)
async def upload_dicom_study(
    patient_id: UUID4 = Form(...),
    file: UploadFile = File(...),
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Endpoint to upload a DICOM file.
    This will be an asynchronous, long-running process.
    """
    if not file.filename.lower().endswith(('.dcm', '.dicom')):
        raise HTTPException(status_code=400, detail="Invalid file type. Only DICOM files are accepted.")
    
    processor = DICOMProcessor(db)
    try:
        result = await processor.process_upload(file, patient_id)
        return result
    except (ValueError, IOError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{task_id}/status")
async def get_task_status(task_id: str, current_user=Depends(get_current_active_user)):
    """Check the status of a background task."""
    task_result = celery_app.AsyncResult(task_id)
    return {
        "task_id": task_id,
        "status": task_result.status,
        "result": task_result.result,
    }