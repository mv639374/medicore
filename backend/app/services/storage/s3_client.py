# What: A client for interacting with our object storage (AWS S3 or, for now, LocalStack). It handles uploading, downloading, and generating temporary URLs for files.
# Why: This abstracts all S3-related logic into one place. Our application code can simply call s3_client.upload_file() without worrying about the underlying boto3 library or AWS credentials. It's also configured to use LocalStack automatically for development.

import logging
import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from app.config import settings
from typing import Optional

logger = logging.getLogger(__name__)

class S3Client:
    def __init__(self):
        s3_config = {
            "aws_access_key_id": settings.AWS_ACCESS_KEY_ID,
            "aws_secret_access_key": settings.AWS_SECRET_ACCESS_KEY,
            "region_name": settings.AWS_REGION,
        }
        # For local development with LocalStack
        if settings.ENVIRONMENT != "production":
            s3_config["endpoint_url"] = settings.AWS_ENDPOINT_URL

        self.s3_client = boto3.client("s3", **s3_config)
        self.bucket_name = settings.AWS_BUCKET_NAME

    def upload_file(self, local_path: str, s3_key: str) -> bool:
        """Uploads a file to the S3 bucket."""
        try:
            self.s3_client.upload_file(
                local_path,
                self.bucket_name,
                s3_key,
                ExtraArgs={"ServerSideEncryption": "AES256"}
            )
            logger.info(f"Successfully uploaded {local_path} to s3://{self.bucket_name}/{s3_key}")
            return True
        except (ClientError, NoCredentialsError) as e:
            logger.error(f"Failed to upload file to S3: {e}")
            return False

    def generate_presigned_url(self, s3_key: str, expiration: int = 3600) -> Optional[str]:
        """Generates a presigned URL to access an S3 object."""
        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket_name, 'Key': s3_key},
                ExpiresIn=expiration
            )
            return url
        except ClientError as e:
            logger.error(f"Failed to generate presigned URL: {e}")
            return None