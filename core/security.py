import bcrypt

from core.errors import UnauthorizedError
from models.response_model import LocationError


# Function to hash the password using bcrypt
async def hash_password(password: str):
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password.decode('utf-8')


# Function to verify password using bcrypt
async def verify_password(plain_password: str, hashed_password: str) -> None:
    if not bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8')):
        raise UnauthorizedError(message="Incorrect username or password", location=LocationError.Body)


# Function to confirm that the user is verified
async def confirmation_verify_user(verified_user: bool) -> None:
    if not verified_user:
        raise UnauthorizedError(message="The user has not been verified", location=LocationError.Body)
