from pydantic import EmailStr, BaseModel

from models.base_models import DBModels


class UsersModel(DBModels):
    _collection_name = 'users'
    username: str
    full_name: str
    email: EmailStr
    password: str
    is_verified: bool = False
    verification_token: str | None
    refresh_token: str | None = None
    password_token: str | None = None


class TokenData(BaseModel):
    id: str
    email: EmailStr
    username: str
    full_name: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'bearer'
