# What: A service dedicated to reading DICOM files. It uses the pydicom library to extract metadata (like Patient ID, Study Date) and the raw pixel data from a DICOM file.
# Why: This isolates the complex logic of DICOM parsing. It provides a clean interface for the rest of our application to get structured information from these medical files without needing to know the low-level details of the DICOM standard.

import logging
import pydicom
import numpy as np
from pydicom.errors import InvalidDicomError

logger = logging.getLogger(__name__)

def parse_dicom_file(file_path: str) -> pydicom.Dataset:
    """Reads and parses a DICOM file."""
    try:
        dicom_dataset = pydicom.dcmread(file_path, force=True)
        return dicom_dataset
    except InvalidDicomError as e:
        logger.error(f"Corrupted or invalid DICOM file at {file_path}: {e}")
        raise ValueError("Invalid DICOM file.")

def get_dicom_metadata(ds: pydicom.Dataset) -> dict:
    """Extracts a structured dictionary of metadata from a DICOM dataset."""
    return {
        "PatientID": ds.get("PatientID", "Unknown"),
        "StudyInstanceUID": ds.get("StudyInstanceUID", "Unknown"),
        "SeriesInstanceUID": ds.get("SeriesInstanceUID", "Unknown"),
        "SOPInstanceUID": ds.get("SOPInstanceUID", "Unknown"),
        "StudyDate": ds.get("StudyDate", ""),
        "StudyTime": ds.get("StudyTime", ""),
        "Modality": ds.get("Modality", "Unknown"),
        "InstitutionName": ds.get("InstitutionName", "N/A"),
        "Manufacturer": ds.get("Manufacturer", "N/A"),
        "StudyDescription": ds.get("StudyDescription", "N/A"),
    }

def extract_image_array(ds: pydicom.Dataset) -> np.ndarray:
    """Extracts and normalizes the pixel array from a DICOM dataset."""
    image_array = ds.pixel_array

    # Apply rescale slope/intercept for proper Hounsfield units (HU) in CTs
    if "RescaleSlope" in ds and "RescaleIntercept" in ds:
        slope = float(ds.RescaleSlope)
        intercept = float(ds.RescaleIntercept)
        image_array = image_array.astype(np.float64) * slope + intercept

    # Handle MONOCHROME1 photometric interpretation (inverted grayscale)
    if ds.get("PhotometricInterpretation") == "MONOCHROME1":
        image_array = np.amax(image_array) - image_array

    return image_array