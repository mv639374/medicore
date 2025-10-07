# What: A service for converting the raw pixel data from a DICOM file into standard image formats like PNG. It also includes image processing functions like applying window/level for contrast adjustment.

# Why: DICOM is a medical format not viewable in a standard web browser. We need to convert images to PNG to generate previews for our frontend application, allowing doctors to quickly see the image.

import numpy as np
import cv2
from PIL import Image
from pydicom.dataset import Dataset

def apply_window_level(image: np.ndarray, window: int, level: int) -> np.ndarray:
    """Applies window and level to a numpy array."""
    min_val = level - window // 2
    max_val = level + window // 2
    image = np.clip(image, min_val, max_val)
    return image

def normalize_to_uint8(image: np.ndarray) -> np.ndarray:
    """Normalizes a numpy array to the 0-255 range (uint8)."""
    if image.max() == image.min():
        return np.zeros_like(image, dtype=np.uint8)
    image = image.astype(np.float64)
    image -= image.min()
    image /= image.max()
    image *= 255.0
    return image.astype(np.uint8)

def dicom_to_png(ds: Dataset, output_path: str) -> str:
    """Converts a DICOM dataset to a PNG image."""
    pixel_array = ds.pixel_array

    # Apply window/level if available
    if "WindowCenter" in ds and "WindowWidth" in ds:
        level = ds.WindowCenter[0] if isinstance(ds.WindowCenter, list) else ds.WindowCenter
        window = ds.WindowWidth[0] if isinstance(ds.WindowWidth, list) else ds.WindowWidth
        pixel_array = apply_window_level(pixel_array, window, level)

    # Normalize and convert to an image
    image_uint8 = normalize_to_uint8(pixel_array)
    pil_image = Image.fromarray(image_uint8)
    pil_image.save(output_path)
    return output_path