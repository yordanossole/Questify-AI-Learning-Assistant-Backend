from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer

from app.db.session import get_db
from app.models.models import User
from app.core.security import decode_jwt
from app.repositories.user_repository import UserRepository
from app.core.exceptions import NotFoundException, ValidationException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    try:
        payload = decode_jwt(token)
        user_id = payload.get("sub")
        if user_id is None:
            raise ValidationException("Invalid token")
    except Exception:
        raise ValidationException("Invalid token")

    repo = UserRepository(db)
    user = repo.get_by_user_id(user_id)
    if not user:
        raise NotFoundException("User not found")

    return user