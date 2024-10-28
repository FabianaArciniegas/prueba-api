from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from core.api_response import ApiResponse
from core.errors import UnauthorizedError
from core.jwt_handler import decode_access_token
from models.response_model import LocationError
from models.users import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/token")


# Add function to extract user from token
async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        api_response: Annotated[ApiResponse, Depends(ApiResponse)]
) -> TokenData:
    payload = decode_access_token(token)
    if not payload or 'id' not in payload:
        raise UnauthorizedError(message="Invalid credentials", location=LocationError.Headers)
    token_data = TokenData(**payload)
    return token_data
