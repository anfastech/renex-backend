from fastapi import APIRouter, HTTPException
import boto3
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI router
router = APIRouter()

# Initialize the S3 client with credentials from environment variables
s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)

@router.get("/generate_presigned_url")
async def generate_presigned_url(file_name: str, file_type: str):
    bucket_name = os.getenv("S3_BUCKET_NAME")

    if not bucket_name:
        raise HTTPException(status_code=500, detail="S3_BUCKET_NAME environment variable is not set.")

    try:
        # Generate presigned URL for uploading file to S3
        presigned_url = s3_client.generate_presigned_url(
            "put_object",
            Params={
                "Bucket": bucket_name,
                "Key": file_name,
                "ContentType": file_type,
            },
            ExpiresIn=3600  # URL expiration time in seconds
        )

        # Log the presigned URL for debugging purposes
        print(f"Generated presigned URL: {presigned_url}")
        return presigned_url
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating presigned URL: {str(e)}")
