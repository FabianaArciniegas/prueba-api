from pydantic import EmailStr, BaseModel


class UserOutput(BaseModel):
    username: str
    full_name: str
    email: EmailStr
