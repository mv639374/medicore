# What: This service validates a DICOM file against our platform's requirements. It checks for the presence of essential metadata tags and ensures the image data is valid.

# Why: This acts as a quality gate. It prevents corrupted, incomplete, or unsupported DICOM files from entering our system, which is crucial for maintaining data integrity and ensuring our AI models receive valid input.

import logging
import pydicom
from app.config import settings

logger = logging.getLogger(__name__)

# Required tags for a DICOM file to be considered valid by our system
REQUIRED_TAGS = [
    "PatientID",
    "StudyInstanceUID",
    "SeriesInstanceUID",
    "SOPInstanceUID",
    "Modality",
]

def validate_dicom_standard(ds: pydicom.Dataset) -> tuple[bool, list[str]]:
    """Validates a DICOM dataset against our platform's standards."""
    errors = []

    # 1. Check for required tags
    for tag in REQUIRED_TAGS:
        if not hasattr(ds, tag) or not getattr(ds, tag):
            errors.append(f"Missing required DICOM tag: {tag}")

    # 2. Check if modality is supported
    modality = ds.get("Modality", "")
    if modality not in settings.DICOM_SUPPORTED_MODALITIES:
        errors.append(f"Unsupported modality: '{modality}'")

    # 3. Validate image data
    try:
        if ds.pixel_array is None or ds.pixel_array.size == 0:
            errors.append("DICOM file contains no pixel data.")
    except Exception as e:
        errors.append(f"Could not read pixel data: {e}")

    is_valid = len(errors) == 0
    return is_valid, errors