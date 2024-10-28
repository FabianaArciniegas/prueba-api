from datetime import datetime, timedelta
from jose import jwt, JWTError, ExpiredSignatureError

from core.config import settings
from core.errors import UnauthorizedError
from models.response_model import LocationError

SECRET_KEY = settings.SECRET_KEY
SECRET_KEY_REFRESH = settings.SECRET_KEY_REFRESH
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7


# Function to create the JWT
def create_access_token(data: dict, expires_delta=None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Function to refresh the JWT
def refresh_access_token(data: dict, expires_delta=None):
    to_encode = data.copy()
    to_encode.update({"type": "refresh"})
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY_REFRESH, ALGORITHM)
    return encoded_jwt


# Function to decode the JWT
def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if not payload.get("id"):
            raise UnauthorizedError(message="Invalid token", location=LocationError.Body)
        return payload
    except ExpiredSignatureError:
        raise UnauthorizedError(message="Token has expired", location=LocationError.Headers)
    except JWTError:
        raise UnauthorizedError(message="Invalid token or signature verification failed",
                                location=LocationError.Headers)


# Function to decode the JWT
def decode_refresh_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY_REFRESH, algorithms=[ALGORITHM])
        if not payload.get("id"):
            raise UnauthorizedError(message="Invalid token", location=LocationError.Body)
        return payload
    except ExpiredSignatureError:
        raise UnauthorizedError(message="Token has expired", location=LocationError.Headers)
    except JWTError:
        raise UnauthorizedError(message="Invalid token or signature verification failed",
                                location=LocationError.Headers)
