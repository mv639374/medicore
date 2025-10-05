from pydantic_settings import BaseSettings
from pydantic import validator

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

    # AWS Configuration
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_BUCKET_NAME: str

    # Application Enviroment
    ENVIRONMENT: str = "development"

    class Config:
        env_file = ".env"

# Create single instance
settings = Settings()