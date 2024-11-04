import re
from pydantic import BaseModel, EmailStr, field_validator
from pydantic_core.core_schema import ValidationInfo

from core.errors import InvalidParameterError
from models.response_model import LocationError


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


class ChangePasswordUserInput(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str

    @field_validator('new_password')
    def validate_password(cls, password):
        if len(password) < 8:
            raise InvalidParameterError(message='Password must be at least 8 characters', location=LocationError.Body)
        if not re.search('[A-Z]', password):
            raise InvalidParameterError(message='Password must contain at least one uppercase letter',
                                        location=LocationError.Body)
        if not re.search('[a-z]', password):
            raise InvalidParameterError(message='Password must contain at least one lowercase letter',
                                        location=LocationError.Body)
        if not re.search('[0-9]', password):
            raise InvalidParameterError(message='Password must contain at least one number',
                                        location=LocationError.Body)
        if not re.search('[!@#$%^&*(),.?\":{}|<>]', password):
            raise InvalidParameterError(message='Password must contain at least one special character',
                                        location=LocationError.Body)
        return password

    @field_validator('confirm_password')
    def password_match(cls, confirm_password, info: ValidationInfo):
        if 'new_password' in info.data and confirm_password != info.data['new_password']:
            raise InvalidParameterError(message='Password must match', location=LocationError.Body)
        return confirm_password
