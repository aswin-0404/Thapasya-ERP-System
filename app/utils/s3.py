import boto3
from botocore.exceptions import NoCredentialsError
from app.core.config import settings

# Initialize the S3 Client
s3_client = boto3.client(
    "s3",
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_S3_REGION,
)

def upload_file_to_s3(file, folder="general"):
    """
    Uploads a file to S3 and returns the public URL.
    """
    bucket_name = settings.AWS_S3_BUCKET_NAME
    # We create a unique path: e.g., courses/violin.jpg
    file_path = f"{folder}/{file.filename}"

    try:
        s3_client.upload_fileobj(
            file.file,
            bucket_name,
            file_path,
            ExtraArgs={
                "ACL": "public-read", # This makes the URL accessible to the website
                "ContentType": file.content_type # Important so browsers don't download it
            }
        )
        
        # Construct the URL
        url = f"https://{bucket_name}.s3.{settings.AWS_S3_REGION}.amazonaws.com/{file_path}"
        return url

    except Exception as e:
        print(f"S3 Upload Error: {e}")
        return None