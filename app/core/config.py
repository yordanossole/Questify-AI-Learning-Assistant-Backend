from pydantic_settings import BaseSettings
from typing import ClassVar

class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str
    GMAIL_APP_PASSWORD: str
    APP_EMAIL: str
    JWT_SECRET_KEY: str
    ENCODING_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    TOKEN_TYPE: str
    HASH_SCHEME: str
    OTP_EXPIRY_MINUTES: int
    SMTP_HOST: str
    SMTP_PORT: int
    MAX_FILE_SIZE: int
    ALLOWED_FILES: ClassVar[set[str]]
    R2_ACCOUNT_ID: str
    R2_ACCESS_KEY: str
    R2_SECRET_KEY: str
    R2_BUCKET_NAME: str
    MATERIAL_FOLDER: str

    @property
    def R2_ENDPOINT_URL(self) -> str:
        return f"https://{self.R2_ACCOUNT_ID}.r2.cloudflarestorage.com"

    class Config:
        env_file = ".env"

settings = Settings() # type: ignore


from dotenv import load_dotenv
import os
load_dotenv()

DATABASE_URL = os.environ['DATABASE_URL']
REDIS_URL = os.environ['REDIS_URL']
GMAIL_APP_PASSWORD = os.environ['GMAIL_APP_PASSWORD']
APP_EMAIL = os.environ['APP_EMAIL']
JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']
ENCODING_ALGORITHM = os.environ['ENCODING_ALGORITHM']
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ['ACCESS_TOKEN_EXPIRE_MINUTES'])
TOKEN_TYPE = os.environ['TOKEN_TYPE']
HASH_SCHEME = os.environ['HASH_SCHEME']
OTP_EXPIRY_MINUTES = int(os.environ['OTP_EXPIRY_MINUTES'])
SMTP_HOST = os.environ['SMTP_HOST']
SMTP_PORT = int(os.environ['SMTP_PORT'])
ALLOWED_FILES = {
    "application/pdf",
    "text/plain",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/rtf",
    "text/markdown",
    "application/vnd.ms-powerpoint",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    "application/vnd.oasis.opendocument.presentation",
    "application/vnd.oasis.opendocument.text",
}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB