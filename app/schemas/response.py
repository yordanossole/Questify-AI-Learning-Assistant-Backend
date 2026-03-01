from uuid import UUID
from datetime import datetime
from typing import Any, Optional
from pydantic import BaseModel, EmailStr

class ApiResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None

class Token(BaseModel):
    access_token: str
    token_type: str

class UserResponse(BaseModel):
    user_id: UUID
    full_name: str
    email: EmailStr
    avatar_url: Optional[str] = None
    is_verified: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }

class MaterialResponse(BaseModel):
    material_id: UUID

    model_config = {
        "from_attributes": True
    }

class CollectionResponse(BaseModel):
    collection_id: UUID
    user_id: UUID
    title: Optional[str] = None
    description: Optional[str] = None
    confidence: float
    created_at: datetime

    model_config = {
        "from_attributes": True
    }