import pytest
import pydicom
from pydicom.dataset import Dataset
import numpy as np

@pytest.fixture
def sample_dicom_dataset():
    ds = Dataset()
    ds.PatientID = "TEST001"
    ds.StudyInstanceUID = "1.2.840.10008.5.1.4.1.1.2"
    ds.SeriesInstanceUID = "1.2.3.4.5.6.7"
    ds.SOPInstanceUID = "1.2.3.4.5.6.7.8"
    ds.Modality = "CT"
    ds.StudyDate = "20251006"
    ds.StudyTime = "120000"
    ds.Rows = 512
    ds.Columns = 512
    ds.PixelData = np.random.randint(0, 255, (512, 512), dtype=np.uint8).tobytes()
    return ds