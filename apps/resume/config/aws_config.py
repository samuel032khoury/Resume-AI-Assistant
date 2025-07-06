import boto3

from .settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION,AWS_STORAGE_BUCKET_NAME,S3_BASE_URL

s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION,
)

AWS_STORAGE_BUCKET_NAME = AWS_STORAGE_BUCKET_NAME
S3_BASE_URL = S3_BASE_URL