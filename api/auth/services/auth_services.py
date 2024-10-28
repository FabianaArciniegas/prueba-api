from motor.motor_asyncio import AsyncIOMotorDatabase

from api.auth.schemas.inputs import UserLogin
from core.api_response import ApiResponse
from core.errors import UnauthorizedError
from core.jwt_handler import create_access_token, refresh_access_token, decode_refresh_token
from core.security import verify_password
from models.response_model import LocationError
from models.users import TokenData, TokenResponse
from repositories.users import UsersRepository


class AuthServices:
    def __init__(self, db: AsyncIOMotorDatabase, api_response: ApiResponse):
        self.db = db
        self.api_response = api_response
        self.users_repository = UsersRepository(self.db, self.api_response)

    async def login_user(self, user_login: UserLogin) -> TokenResponse:
        self.api_response.logger.info('Getting user in db')
        user = await self.users_repository.get_user_by_username(user_login.username)
        await verify_password(user_login.password, user.password)

        token_data = TokenData(**user.model_dump())
        access_token = create_access_token(data=token_data.model_dump())
        refresh_token = refresh_access_token(data=token_data.model_dump())
        user.refresh_token = refresh_token

        await self.users_repository.patch(user.id, user)
        self.api_response.logger.info(f'User logged in service')
        return TokenResponse(access_token=access_token, refresh_token=refresh_token)

    async def refresh_token(self, refresh_token_user: str) -> TokenResponse:
        self.api_response.logger.info('Verifying refresh token')
        payload = decode_refresh_token(refresh_token_user)

        user = await self.users_repository.get_by_id(payload.get("id"))

        if not refresh_token_user == user.refresh_token:
            raise UnauthorizedError(message="Invalid token", location=LocationError.Body)

        token_data = TokenData(**user.model_dump())
        new_access_token = create_access_token(data=token_data.model_dump())
        new_refresh_token = refresh_access_token(data=token_data.model_dump())
        user.refresh_token = new_refresh_token

        await self.users_repository.patch(user.id, user)
        self.api_response.logger.info(f'Token refreshed in service')
        return TokenResponse(access_token=new_access_token, refresh_token=new_refresh_token)

    async def logout_user(self, user_id: str):
        self.api_response.logger.info('Getting user in db')
        user = await self.users_repository.get_by_id(user_id)
        user.refresh_token = None
        await self.users_repository.patch(user.id, user)
        self.api_response.logger.info(f'User logged out in service')

    async def auth_user_token(self, form_data) -> TokenResponse:
        self.api_response.logger.info('Getting user in db')
        user = await self.users_repository.get_user_by_username(form_data.username)
        await verify_password(form_data.password, user.password)

        token_data = TokenData(**user.model_dump())
        access_token = create_access_token(data=token_data.model_dump())
        refresh_token = refresh_access_token(data=token_data.model_dump())

        self.api_response.logger.info(f'User authenticated in service')
        return TokenResponse(access_token=access_token, refresh_token=refresh_token)
