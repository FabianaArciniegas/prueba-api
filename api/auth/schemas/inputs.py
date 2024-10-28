from pydantic import BaseModel


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    token: str
