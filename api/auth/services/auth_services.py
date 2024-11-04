from motor.motor_asyncio import AsyncIOMotorDatabase
from pydantic import EmailStr

from api.auth.schemas.inputs import UserLogin, ResetPasswordUserInput
from api.users.schemas.inputs import UserBasic
from core.api_response import ApiResponse
from core.errors import UnauthorizedError
from core.jwt_handler import create_random_token, decode_token, TokenType, create_token
from core.security import verify_password, hash_password, confirmation_verify_user
from models.response_model import LocationError
from models.users import TokenData, TokenResponse
from repositories.users import UsersRepository
from services.email_sending_service import EmailService


class AuthServices:
    def __init__(self, db: AsyncIOMotorDatabase, api_response: ApiResponse):
        self.db = db
        self.api_response = api_response
        self.users_repository = UsersRepository(self.db, self.api_response)
        self.email_service = EmailService()

    async def login_user(self, user_login: UserLogin) -> TokenResponse:
        self.api_response.logger.info('Getting user in db')
        user = await self.users_repository.get_user_by_username(user_login.username)
        await verify_password(user_login.password, user.password)
        await confirmation_verify_user(user.is_verified)

        token_data = TokenData(**user.model_dump())
        access_token = create_token(data=token_data.model_dump(), token_type=TokenType.ACCESS_TOKEN)
        refresh_token = create_token(data=token_data.model_dump(), token_type=TokenType.REFRESH_TOKEN)
        user.refresh_token = refresh_token

        await self.users_repository.patch(user.id, user)
        self.api_response.logger.info(f'User logged in service')
        return TokenResponse(access_token=access_token, refresh_token=refresh_token)

    async def refresh_token(self, refresh_token_user: str) -> TokenResponse:
        self.api_response.logger.info('Verifying refresh token')
        payload = decode_token(refresh_token_user, TokenType.REFRESH_TOKEN)

        user = await self.users_repository.get_by_id(payload.get("id"))

        if not refresh_token_user == user.refresh_token:
            raise UnauthorizedError(message="Invalid token", location=LocationError.Body)

        token_data = TokenData(**user.model_dump())
        new_access_token = create_token(data=token_data.model_dump(), token_type=TokenType.ACCESS_TOKEN)
        new_refresh_token = create_token(data=token_data.model_dump(), token_type=TokenType.REFRESH_TOKEN)
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
        access_token = create_token(data=token_data.model_dump(), token_type=TokenType.ACCESS_TOKEN)
        refresh_token = create_token(data=token_data.model_dump(), token_type=TokenType.REFRESH_TOKEN)

        self.api_response.logger.info(f'User authenticated in service')
        return TokenResponse(access_token=access_token, refresh_token=refresh_token)

    async def forgot_password(self, email_user: EmailStr) -> None:
        self.api_response.logger.info('Getting user in db')
        user = await self.users_repository.get_user_by_email(email_user)

        password_reset_token = create_random_token()
        self.api_response.logger.info(f'Password reset created token')

        user.password_token = password_reset_token
        await self.users_repository.patch(user.id, user)

        await self.email_service.create_password_reset_message(user.id, email_user, password_reset_token)
        self.api_response.logger.info(f'Password reset email sent successfully')

    async def reset_password(self, password_data: ResetPasswordUserInput) -> UserBasic:
        self.api_response.logger.info('Getting user in db')
        user_found = await self.users_repository.get_by_id(password_data.user_id)

        self.api_response.logger.info("Verify that the authenticated user can only access")
        if not user_found.password_token == password_data.token_password_reset:
            raise UnauthorizedError(message="Invalid token", location=LocationError.Body)

        hashed_password = await hash_password(password_data.new_password)
        user_found.password = hashed_password
        user_found.password_token = None

        user_updated = await self.users_repository.patch(user_found.id, user_found)
        user = UserBasic(**user_updated.model_dump())
        self.api_response.logger.info(f'Password updated in service')
        return user
