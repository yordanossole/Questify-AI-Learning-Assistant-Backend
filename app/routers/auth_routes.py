from typing import Annotated
from starlette import status
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm

from app.db.session import get_db
from app.models.models import User
from app.schemas.response import UserResponse
from app.core.response import success_response
from app.services.auth_service import AuthService
from app.core.dependencies import get_current_user
from app.repositories.user_repository import UserRepository
from app.schemas.request import LoginRequest, RegisterRequest, VerifyAccountRequest, GetOTPRequest

router = APIRouter()

@router.post("/register")
def register(payload: RegisterRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    repo = UserRepository(db)
    service = AuthService(repo)
    email_payload = service.register(payload.full_name, payload.email, payload.password)

    background_tasks.add_task(service.send_registration_otp, **email_payload)

    return success_response("OTP sent to your email", status_code=status.HTTP_201_CREATED)

@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    repo = UserRepository(db)
    service = AuthService(repo)
    token = service.login(email=payload.email, password=payload.password)

    return success_response("Login successfull", token)

@router.post("/verify")
def verify_account(payload: VerifyAccountRequest, db: Session = Depends(get_db)):
    repo = UserRepository(db)
    service = AuthService(repo)
    service.verify_account(payload.email, payload.otp)
    return success_response("Account verified successfully")

@router.post("/resend-otp")
def resend_otp(payload: GetOTPRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    repo = UserRepository(db)
    service = AuthService(repo)
    email_payload = service.resend_registration_otp(payload.email)

    background_tasks.add_task(service.send_registration_otp, **email_payload)
    return success_response("OTP sent to your email")

@router.get("/user/profile")
def my_profile(current_user: Annotated[User, Depends(get_current_user)]):
    user_data = UserResponse.model_validate(current_user)
    return success_response("User profile fetched", data=user_data)

# Used for SwaggerUI only
@router.post("/token")
def token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    repo = UserRepository(db)
    service = AuthService(repo)
    token = service.login(email=form_data.username, password=form_data.password)

    return token