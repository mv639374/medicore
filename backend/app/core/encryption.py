# What: This file contains simple functions to encrypt and decrypt data using a symmetric key.

# Why: This is for HIPAA compliance. We will use these functions to encrypt sensitive patient data (like name and SSN) before saving it to the database, ensuring the data is protected even if the database itself is compromised.

from cryptography.fernet import Fernet

from backend.app.config import settings

# Initialize the cipher suite with the key with settings
cipher_suite = Fernet(settings.ENCRYPTION_KEY.encode())


def encrypt_data(data: str) -> bytes:
    """Encrypts a string and returns bytes."""
    return cipher_suite.encrypt(data.encode())


def decrypt_data(encrypted_data: bytes) -> str:
    """Decryptes bytes and returns a string."""
    return cipher_suite.decrypt(encrypted_data).decode()
