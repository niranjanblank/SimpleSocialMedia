import boto3
from dotenv import load_dotenv
import os
from fastapi import UploadFile, HTTPException

# load env variables
load_dotenv()

# retrieve data from env
BUCKET_NAME = os.getenv('AWS_S3_BUCKET_NAME')
DEFAULT_IMAGE_URL = os.getenv("DEFAULT_IMAGE_URL")
REGION = os.getenv('AWS_REGION')

s3_client = boto3.client('s3')


def upload_to_s3(file: UploadFile, object_name: str, bucket_name: str = BUCKET_NAME, region: str = REGION):
    """Upload the file s3 bucket"""
    try:
        s3_client.upload_fileobj(file.file, bucket_name, object_name)
        return f"https://{bucket_name}.s3.{region}.amazonaws.com/{object_name}"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not upload image: {e}")


def list_template_images(prefix: str, bucket_name: str = BUCKET_NAME, region: str = REGION):
    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
        if 'Contents' in response:
            return [
                f"https://{bucket_name}.s3.{region}.amazonaws.com/{item['Key']}"
                for item in response['Contents']
                if item['Key'] != prefix  # Exclude the prefix directory itself
            ]
        return []
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not list objects: {e}")
