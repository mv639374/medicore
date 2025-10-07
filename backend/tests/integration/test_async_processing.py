import pytest
from unittest.mock import patch, MagicMock
from uuid import uuid4

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.models.database.study import DICOMStudy
from app.dependencies import get_db

# This is a test database override. It's a more advanced testing pattern.
# For now, we are mocking the database directly in the test.

@pytest.fixture
def client():
    return TestClient(app)

# We use 'patch' to mock the entire DICOMProcessor and the Celery task.
# This lets us test the API endpoint in isolation.
@patch('app.api.v1.endpoints.studies.DICOMProcessor')
@patch('app.api.v1.endpoints.studies.process_dicom_async.delay')
def test_upload_dicom_study_success(self, mock_celery_delay, mock_processor_class, client):
    """
    Tests the /upload endpoint, mocking the processor and celery task.
    """
    # Arrange
    mock_task = MagicMock()
    mock_task.id = "test_task_id"
    mock_celery_delay.return_value = mock_task

    mock_processor_instance = mock_processor_class.return_value
    mock_processor_instance.process_upload.return_value = {
        "study_id": uuid4(),
        "task_id": "test_task_id",
        "status": "processing_started"
    }

    file_content = b"fake dicom data"
    patient_id = uuid4()
    files = {'file': ('test.dcm', file_content, 'application/dicom')}
    data = {'patient_id': str(patient_id)}

    # Act
    response = client.post("/api/v1/studies/upload", files=files, data=data)

    # Assert
    assert response.status_code == 202
    json_response = response.json()
    assert json_response["status"] == "processing_started"
    assert json_response["task_id"] == "test_task_id"