import secrets
from datetime import datetime, timedelta
from enum import Enum
from jose import jwt, JWTError, ExpiredSignatureError

from core.config import settings
from core.errors import UnauthorizedError
from models.response_model import LocationError

SECRET_KEY = settings.SECRET_KEY
SECRET_KEY_REFRESH = settings.SECRET_KEY_REFRESH
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7


class TokenType(str, Enum):
    ACCESS_TOKEN = "access_token"
    REFRESH_TOKEN = "refresh_token"


# Function to create the JWT
def create_token(data: dict, token_type: TokenType):
    to_encode = data.copy()
    if token_type == TokenType.ACCESS_TOKEN:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    if token_type == TokenType.REFRESH_TOKEN:
        expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY_REFRESH, ALGORITHM)
    return encoded_jwt


# Function to decode the JWT
def decode_token(token: str, token_type: TokenType):
    try:
        if token_type == TokenType.ACCESS_TOKEN:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if token_type == TokenType.REFRESH_TOKEN:
            payload = jwt.decode(token, SECRET_KEY_REFRESH, algorithms=[ALGORITHM])

        if not payload.get("id"):
            raise UnauthorizedError(message="Invalid token", location=LocationError.Body)
        return payload
    except ExpiredSignatureError:
        raise UnauthorizedError(message="Token has expired", location=LocationError.Headers)
    except JWTError:
        raise UnauthorizedError(message="Invalid token or signature verification failed",
                                location=LocationError.Headers)


# Function to create random token
def create_random_token():
    return secrets.token_urlsafe()
