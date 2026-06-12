from datetime import datetime, timezone, timedelta
from pwdlib import PasswordHash
import jwt
from jwt.exceptions import InvalidTokenError
from src.config import settings

password_hash = PasswordHash.recommended()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)


def password_hasher(plain_password: str) -> str:
    return password_hash.hash(plain_password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.AUTH_ACCESS_TOKEN_DURATION)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.AUTH_DPOP_SECRET_KEY, algorithm=settings.AUTH_DPOP_ALGORITHM)
    return encoded_jwt

def decode_token(token: str) -> dict:
    return jwt.decode(token, settings.AUTH_DPOP_SECRET_KEY, algorithms=[settings.AUTH_DPOP_ALGORITHM])
   
