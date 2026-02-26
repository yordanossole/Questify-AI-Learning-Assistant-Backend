from typing import Union 
from pydantic import field_validator, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

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
    ALLOWED_FILES: Union[set[str], str] = Field(default_factory=set)
    R2_ACCOUNT_ID: str
    R2_ACCESS_KEY: str
    R2_SECRET_KEY: str
    R2_BUCKET_NAME: str
    MATERIAL_FOLDER: str
    MAX_FILE_SIZE_MB: int

    model_config = SettingsConfigDict(env_file=".env")

    @property
    def R2_ENDPOINT_URL(self) -> str:
        return f"https://{self.R2_ACCOUNT_ID}.r2.cloudflarestorage.com"
    
    @property
    def MAX_FILE_SIZE_BYTES(self) -> int:
        return self.MAX_FILE_SIZE_MB * 1024 * 1024
    
    @field_validator("ALLOWED_FILES", mode="before")
    @classmethod
    def parse_allowed_files(cls, v):
        if isinstance(v, str):
            return {item.strip() for item in v.split(",") if item.strip()}
        return v
    

settings = Settings() # type: ignore