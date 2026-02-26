import secrets

from app.schemas.response import Token
from app.repositories.user_repository import UserRepository
from app.core.config import settings
from app.core.security import verify_password, create_access_token, hash_password
from app.core.exceptions import InvalidCredentials, AlreadyExistsException, NotFoundException, AppException, BadRequestException
from app.models.models import User
from app.infrastructure.mailer import Mailer
from app.infrastructure.otp_manager import OTPManager

class AuthService:
    def __init__(self, repository: UserRepository):
        self.repo = repository
        self.mailer = Mailer()
        self.otp_manager = OTPManager()

    def send_registration_otp(self, email: str, otp: str, full_name: str):
        subject = "Verify your email"
        template = "otp_verification.html"
        context = {"full_name": full_name, "otp": otp, "expiry_minutes": settings.OTP_EXPIRY_MINUTES}
        self.mailer.send_email(email, subject, template, context)

    def verify_account(self, email: str, otp: str):
        user = self.repo.get_by_email(email)
        if not user:
            raise NotFoundException("User not created")

        if user.is_verified:
            raise AppException(f"Email: {email} already verified")

        key = f"registration:{email}"
        stored_otp = self.otp_manager.get_otp(key)
        if stored_otp != otp:
            raise AppException("Verification code expired, or invalid")

        self.otp_manager.delete_otp(key)
        return self.repo.verify_user(user)

    def login(self, email: str, password: str):
        user = self.repo.get_by_email(email)

        if not user or not verify_password(password, user.password_hash):
            raise InvalidCredentials("Incorrect Email or Password")

        token = create_access_token({"sub": str(user.user_id)})
        return Token(access_token=token, token_type="bearer")

    def register(self, full_name: str, email: str, password: str):
        if self.repo.get_by_email(email):
            raise AlreadyExistsException("Email already registered")
        
        user = User(full_name=full_name, email=email, password_hash=hash_password(password))
        self.repo.create(user)

        otp = self._generate_and_store_otp(email, type="registration")
        return self._email_payload(user, otp)

    def resend_registration_otp(self, email: str):
        user = self.repo.get_by_email(email)
        if not user:
            raise NotFoundException("User not found")
        
        if user.is_verified:
            raise BadRequestException("Account already verified")
        
        otp = self._generate_and_store_otp(email, type="registration")
        return self._email_payload(user, otp)
        
    def _email_payload(self, user: User, otp: str):
        return {
            "otp": otp,
            "email": user.email,
            "full_name": user.full_name,
        }

    def _generate_and_store_otp(self, email: str, type: str):
        otp = str(secrets.randbelow(10**6)).zfill(6)
        self.otp_manager.save_otp(f"{type}:{email}", otp)
        return otp