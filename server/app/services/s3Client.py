import boto3
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION"),
)

BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

def generate_unique_filename(prefix: str, extension: str) -> str:
    """Generate a unique filename using the current timestamp."""
    timestamp = datetime.now(datetime.UTC).strftime("%Y%m%d_%H%M%S")
    return f"{prefix}/{timestamp}.{extension}"

def generate_presigned_upload_url(key: str, expiration: int = 3600):
    """Generate a presigned S3 URL for uploading a file."""
    try:
        url = s3_client.generate_presigned_url(
            "put_object",
            Params={"Bucket": BUCKET_NAME, "Key": key},
            ExpiresIn=expiration,
        )
        return url
    except Exception as e:
        print(f"Error generating presigned URL: {e}")
        raise

def generate_presigned_download_url(key: str, expiration: int = 3600):
    """Generate a presigned S3 URL for downloading a file."""
    try:
        url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": BUCKET_NAME, "Key": key},
            ExpiresIn=expiration,
        )
        return url
    except Exception as e:
        print(f"Error generating presigned URL: {e}")
        raise

