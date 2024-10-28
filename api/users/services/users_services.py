from motor.motor_asyncio import AsyncIOMotorDatabase

from api.users.schemas.inputs import UserInput, PatchUserInput
from core.api_response import ApiResponse
from core.security import hash_password
from models.users import UsersModel, TokenData
from repositories.users import UsersRepository
from utils.auth import verify_user


class UsersService:
    def __init__(self, db: AsyncIOMotorDatabase, api_response: ApiResponse, token_data: TokenData | None = None):
        self.db = db
        self.api_response = api_response
        self.token_data = token_data
        self.users_repository = UsersRepository(self.db, self.api_response)

    async def create_user(self, user_input: UserInput) -> UsersModel:
        self.api_response.logger.info('Check user in db')
        await self.users_repository.check_if_the_username_exists(user_input.username)

        hashed_password = await hash_password(user_input.password)
        user_data = user_input.model_dump()
        user_data['password'] = hashed_password

        user_created = await self.users_repository.create(user_data)
        self.api_response.logger.info(f'User created in service')
        return user_created

    async def get_user_by_id(self, user_id: str) -> UsersModel:
        self.api_response.logger.info("Verify that the authenticated user can only access their own information")
        verify_user(user_id, self.token_data)

        self.api_response.logger.info('Getting user in db')
        user_found = await self.users_repository.get_by_id(user_id)
        self.api_response.logger.info(f'User found in service')
        return user_found

    async def get_all_users(self) -> list[UsersModel]:
        self.api_response.logger.info('Getting all users in db')
        all_users = await self.users_repository.get_all()
        self.api_response.logger.info(f'All users found in service')
        return all_users

    async def update_user(self, user_id: str, update_data: PatchUserInput) -> UsersModel:
        self.api_response.logger.info("Verify that the authenticated user can only access their own information")
        verify_user(user_id, self.token_data)

        self.api_response.logger.info('Getting user in db')
        await self.users_repository.check_if_the_username_exists(update_data.username)
        await self.users_repository.get_by_id(user_id)

        user_updated = await self.users_repository.patch(user_id, update_data)
        self.api_response.logger.info(f'User updated data in service')
        return user_updated

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
