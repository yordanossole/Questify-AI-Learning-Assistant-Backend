import uuid

from fastapi import UploadFile
from botocore.exceptions import ClientError

from app.core.storage import get_r2_client
from app.core.config import settings
from app.core.exceptions import ExternalServiceException

class FileService():
    async def save_document(self, file: UploadFile, new_file_name: str, file_type: str, folder: str) -> str:
        async with get_r2_client() as s3:
            try:
                content = await file.read()
                file_name = f"{folder}/{uuid.uuid4()}-{new_file_name}"
                await s3.put_object(
                    Bucket=settings.R2_BUCKET_NAME,
                    Key=file_name,
                    Body=content,
                    ContentType=file_type,
                )
                return file_name
            except ClientError as e:
                raise ExternalServiceException(str(e))
            finally:
                await file.close()

    async def delete_document(self, file_key: str):
        async with get_r2_client() as s3:
            try:
                await s3.delete_object(
                    Bucket=settings.R2_BUCKET_NAME,
                    Key=file_key)
            except ClientError as e:
                raise ExternalServiceException(str(e)) 

    async def get_document(self, file_key: str):
        async with get_r2_client() as s3:
            try:
                response = await s3.get_object(
                    Bucket=settings.R2_BUCKET_NAME,
                    Key=file_key,
                )
                file_bytes = await response["Body"].read()
                data = {
                    "file_bytes": file_bytes,
                    "content_type": response.get("ContentType"),
                    "file_name": file_key
                }

                return data
            except ClientError as e:
                raise ExternalServiceException(str(e))