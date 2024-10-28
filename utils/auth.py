from core.errors import UnauthorizedError
from models.response_model import LocationError
from models.users import TokenData


def verify_user(user_id: str, token_data: TokenData):
    if user_id != token_data.id:
        raise UnauthorizedError(message="Access denied: You are not allowed to access this resource",
                                location=LocationError.Body)
