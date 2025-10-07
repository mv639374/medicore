from pydantic import validator
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """
    Manages application configuration using Pydantic.
    It reads enviroment variables from a .env file.
    """

    # Database configuration
    DATABASE_HOST: str
    DATABASE_PORT: int = 5432
    DATABASE_NAME: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str

    @property
    def DATABASE_URL(self) -> str:
        """Constructs the database URL from individual components."""
        return f"postgresql://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"

    # Redis Configuration
    REDIS_URL: str

    # Security - JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = 30

    # New security settings
    ENCRYPTION_KEY: str

    # AWS Configuration
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION: str = "ap-south-1"
    AWS_BUCKET_NAME: str
    AWS_ENDPOINT_URL: Optional[str] = None # For LocalStack

    # DICOM Processing Configuration
    DICOM_TEMP_DIR: str = "/tmp/dicom"
    DICOM_SUPPORTED_MODALITIES: list[str] = ["CT", "MR", "CR", "DX", "MG", "US"]

    # Application Enviroment
    ENVIRONMENT: str = "development"

    # Rate limiting
    RATE_LIMIT_ENABLED: bool = True

    # CORS configuration
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]
    CORS_ALLOW_CREDENTIALS: bool = True

    # API configuration
    API_V1_PERFIX: str = "/api/v1"
    OPENAPI_URL: str = "/api/v1/openapi.json"

    # Celery Configuration
    @property
    def CELERY_BROKER_URL(self) -> str:
        return self.REDIS_URL

    @property
    def CELERY_RESULT_BACKEND(self) -> str:
        return self.REDIS_URL

    class Config:
        env_file = ".env"
        extra = "ignore"


# Create single instance
settings = Settings()
