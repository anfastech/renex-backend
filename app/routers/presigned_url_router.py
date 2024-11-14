from fastapi import APIRouter, HTTPException, Query
from typing import Any
import boto3
import os

router = APIRouter()

# Initialize S3 client
s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)

@router.get("/generate_presigned_url", response_model=str)
async def generate_presigned_url(file_name: str = Query(...), file_type: str = Query(...)) -> Any:
    """Generate a pre-signed URL to allow file upload directly to S3."""
    bucket_name = os.getenv("S3_BUCKET_NAME")

    if not bucket_name:
        raise HTTPException(status_code=500, detail="S3_BUCKET_NAME environment variable is not set.")
    
    try:
        presigned_url = s3_client.generate_presigned_url(
            ClientMethod="put_object",
            Params={
                "Bucket": bucket_name,
                "Key": file_name,
                "ContentType": file_type
            },
            ExpiresIn=3600  # URL expires in 1 hour
        )
        return presigned_url
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate pre-signed URL: {e}")
