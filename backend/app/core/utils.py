import uuid
import hashlib
from datetime import datetime
from typing import Optional

def generate_unique_filename(original_filename: str) -> str:
    """Creates a unique filename based on a timestamp and UUID."""
    extension = original_filename.split('.')[-1]
    unique_id = uuid.uuid4()
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    return f"{timestamp}_{unique_id}.{extension}"

def format_dicom_date(dicom_date: str) -> Optional[datetime.date]:
    """Converts DICOM date format (YYYYMMDD) to a date object."""
    if not dicom_date:
        return None
    try:
        return datetime.strptime(dicom_date, '%Y%m%d').date()
    except (ValueError, TypeError):
        return None