from pydantic import EmailStr

from models.base_models import DBModels


class UsersModel(DBModels):
    _collection_name = 'users'
    username: str
    full_name: str
    email: EmailStr
    hashed_password: str
