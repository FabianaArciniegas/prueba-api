from pydantic import BaseModel, EmailStr


class UserBasic(BaseModel):
    username: str
    full_name: str
    email: EmailStr


class UserInput(UserBasic):
    password: str


class PatchUserInput(BaseModel):
    username: str | None = None
    full_name: str | None = None
    email: EmailStr | None = None
