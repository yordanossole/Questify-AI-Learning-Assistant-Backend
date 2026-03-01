from typing import Annotated
from pydantic import BaseModel, EmailStr
from pydantic.types import StringConstraints

class RegisterRequest(BaseModel):
    full_name: str
    email: EmailStr
    password: Annotated[str, StringConstraints(min_length=8)]

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class GetOTPRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    new_password: Annotated[str, StringConstraints(min_length=8)]

class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: Annotated[str, StringConstraints(min_length=8)]

class VerifyAccountRequest(BaseModel):
    otp: str
    email: EmailStr

class MaterialsRequest(BaseModel):
    material_ids: list[str]