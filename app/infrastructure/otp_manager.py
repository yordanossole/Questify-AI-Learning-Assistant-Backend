from datetime import timedelta

from app.infrastructure.redis_client import redis_client
from app.core.config import settings

class OTPManager:

    @staticmethod
    def save_otp(key: str, otp: str):
        redis_client.setex(key, timedelta(minutes=settings.OTP_EXPIRY_MINUTES), otp)

    @staticmethod
    def delete_otp(key: str):
        redis_client.delete(key)

    @staticmethod
    def get_otp(key: str):
        return redis_client.get(key)