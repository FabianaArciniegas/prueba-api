from motor.motor_asyncio import AsyncIOMotorDatabase

from api.users.schemas.inputs import UserInput, PatchUserInput, UserBasic, ChangePasswordUserInput
from core.api_response import ApiResponse
from core.errors import UnauthorizedError
from core.jwt_handler import create_random_token
from core.security import hash_password, verify_password
from models.response_model import LocationError
from models.users import TokenData
from repositories.users import UsersRepository
from services.email_sending_service import EmailService
from utils.auth import verify_user


class UsersService:
    def __init__(self, db: AsyncIOMotorDatabase, api_response: ApiResponse, token_data: TokenData | None = None):
        self.db = db
        self.api_response = api_response
        self.token_data = token_data
        self.users_repository = UsersRepository(self.db, self.api_response)
        self.email_service = EmailService()

    async def create_user(self, user_input: UserInput) -> UserBasic:
        self.api_response.logger.info('Check user in db')
        await self.users_repository.check_if_the_username_exists(user_input.username)

        hashed_password = await hash_password(user_input.password)
        user_data = user_input.model_dump()
        user_data['password'] = hashed_password

        user_confirmation_token = create_random_token()
        user_data["verification_token"] = user_confirmation_token

        user_created = await self.users_repository.create(user_data)

        await self.email_service.create_verify_email_message(user_created.id, user_created.email,
                                                             user_confirmation_token)

        user = UserBasic(**user_created.model_dump())
        self.api_response.logger.info(f'User created in service')
        return user

    async def verify_email(self, user_id: str, user_verification_token: str) -> None:
        self.api_response.logger.info('Check user in db')
        user_found = await self.users_repository.get_by_id(user_id)

        self.api_response.logger.info("Verify that the authenticated user can only access")
        if not user_found.verification_token == user_verification_token:
            raise UnauthorizedError(message="Invalid token", location=LocationError.Body)

        user_found.is_verified = True
        user_found.verification_token = None
        await self.users_repository.patch(user_id, user_found)
        self.api_response.logger.info(f'User verified in db')

    async def get_user_by_id(self, user_id: str) -> UserBasic:
        self.api_response.logger.info("Verify that the authenticated user can only access their own information")
        verify_user(user_id, self.token_data)

        self.api_response.logger.info('Getting user in db')
        user_found = await self.users_repository.get_by_id(user_id)
        user = UserBasic(**user_found.model_dump())
        self.api_response.logger.info(f'User found in service')
        return user

    async def get_all_users(self) -> list[UserBasic]:
        self.api_response.logger.info('Getting all users in db')
        all_users = await self.users_repository.get_all()
        users = [UserBasic(**user.model_dump()) for user in all_users]
        self.api_response.logger.info(f'All users found in service')
        return users

    async def update_user(self, user_id: str, update_data: PatchUserInput) -> UserBasic:
        self.api_response.logger.info("Verify that the authenticated user can only access their own information")
        verify_user(user_id, self.token_data)

        self.api_response.logger.info('Getting user in db')
        await self.users_repository.check_if_the_username_exists(update_data.username)
        await self.users_repository.get_by_id(user_id)

        user_updated = await self.users_repository.patch(user_id, update_data)
        user = UserBasic(**user_updated.model_dump())
        self.api_response.logger.info(f'User updated data in service')
        return user

    async def disable_user(self, user_id: str) -> None:
        self.api_response.logger.info("Verify that the authenticated user can only access their own information")
        verify_user(user_id, self.token_data)

        self.api_response.logger.info('Getting user in db')
        user = await self.users_repository.get_by_id(user_id)
        user.is_deleted = True
        user.refresh_token = None

        await self.users_repository.disable(user_id, user.model_dump())
        self.api_response.logger.info(f'User disabled in service')

    async def delete_user(self, user_id: str) -> None:
        self.api_response.logger.info("Verify that the authenticated user can only access their own information")
        verify_user(user_id, self.token_data)

        await self.users_repository.delete(user_id)
        self.api_response.logger.info(f'User deleted in service')

    async def change_password(self, user_id: str, update_data: ChangePasswordUserInput) -> UserBasic:
        self.api_response.logger.info("Verify that the authenticated user can only access their own information")
        verify_user(user_id, self.token_data)

        self.api_response.logger.info('Getting user in db')
        user_found = await self.users_repository.get_by_id(user_id)
        await verify_password(update_data.current_password, user_found.password)
        hashed_password = await hash_password(update_data.new_password)
        user_found.password = hashed_password

        user_updated = await self.users_repository.patch(user_id, user_found)
        user = UserBasic(**user_updated.model_dump())
        self.api_response.logger.info(f'Password updated in service')
        return user
