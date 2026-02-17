from jwt import encode, decode
from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError

from app.core.exceptions import ValidationException
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES, JWT_SECRET_KEY, ENCODING_ALGORITHM

pwd_context = PasswordHash.recommended()

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str):
    return pwd_context.verify(password, hashed)

def create_access_token(data: dict):
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data.update({"exp": expire})
    return encode(data, JWT_SECRET_KEY, algorithm=ENCODING_ALGORITHM)

def decode_jwt(token: str):
    try:
        return decode(token, JWT_SECRET_KEY, algorithms=ENCODING_ALGORITHM)
    except ExpiredSignatureError:
        raise ValidationException("Token expired")
    except InvalidTokenError:
        raise ValidationException("Invalid token")