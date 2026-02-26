import aioboto3

from contextlib import asynccontextmanager
from typing import AsyncIterator, Any
from app.core.config import settings

session = aioboto3.Session()

@asynccontextmanager
async def get_r2_client() -> AsyncIterator[Any]:
    async with session.client( # type: ignore
        "s3",
        endpoint_url=settings.R2_ENDPOINT_URL,
        aws_access_key_id=settings.R2_ACCESS_KEY,
        aws_secret_access_key=settings.R2_SECRET_KEY,
        region_name="auto",
    ) as client:
        yield client