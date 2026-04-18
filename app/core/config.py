from pydantic_settings import BaseSettings

import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

DATABASE_URL=os.getenv("DATABASE_URL")

ADMIN_USERNAME=os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD=os.getenv("ADMIN_PASSWORD")
ADMIN_EMAIL=os.getenv("ADMIN_EMAIL")

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_S3_BUCKET_NAME: str
    AWS_S3_REGION: str = "ap-south-1"

    class Config:
        env_file = ".env"
        extra = "ignore" 

settings = Settings()