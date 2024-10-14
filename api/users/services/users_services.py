from datetime import datetime

from motor.motor_asyncio import AsyncIOMotorDatabase

from api.users.schemas.inputs import UserInput, PatchUserInput, UserBasic
from core.api_response import ApiResponse
from models.users import UsersModel
from repositories.users import UsersRepository


class UsersService:
    def __init__(self, db: AsyncIOMotorDatabase, api_response: ApiResponse):
        self.db = db
        self.api_response = api_response
        self.users_repository = UsersRepository(self.db)

    async def password_hasher(self, raw_password: str):
        return 'secret' + raw_password

    async def create_user(self, user_input: UserInput):
        print('Check user in db')
        await self.users_repository.check_if_the_user_exists(user_input.username)

        hashed_password = await self.password_hasher(user_input.password)
        user_data = user_input.model_dump()
        user_data['hashed_password'] = hashed_password
        user_created = await self.users_repository.create(user_data)
        print(f'User created in service')
        return user_created

    async def get_user_by_id(self, user_id: str) -> UsersModel:
        self.api_response.logger.log_info('Getting user in db')
        user_found = await self.users_repository.get_by_id(user_id)
        self.api_response.logger.log_info(f'User found in service')
        return user_found

    async def get_all_users(self) -> list[UsersModel]:
        print('Getting all users in db')
        all_users = await self.users_repository.get_all()
        print(f'All users found in service')
        return all_users

    async def update_user(self, user_id: str, update_data: PatchUserInput) -> UsersModel:
        print('Getting user in db')
        await self.users_repository.get_by_id(user_id)
        await self.users_repository.check_if_the_user_exists(update_data.username)

        user_updated = await self.users_repository.update(user_id, update_data.model_dump())
        print(f'User updated data in service')
        return user_updated

    async def update_all_user(self, user_id: str, update_user: UserBasic) -> UsersModel:
        print('Getting user in db')
        user = await self.users_repository.get_by_id(user_id)
        await self.users_repository.check_if_the_user_exists(update_user.username)

        user.update_at = datetime.utcnow()
        user.username = update_user.username
        user.email = update_user.email
        user.full_name = update_user.full_name
        user_all_updated = await self.users_repository.update_all(user_id, user.model_dump())
        print(f'User all updated in service')
        return user_all_updated

    async def disable_user(self, user_id: str):
        print('Getting user in db')
        user = await self.users_repository.get_by_id(user_id)
        user.is_deleted = True

        user_disabled = await self.users_repository.disable(user_id, user.model_dump())
        print(f'User disabled in service')
        return user_disabled

    async def delete_user(self, user_id: str):
        print('Getting user in db')
        await self.users_repository.get_by_id(user_id)

        user_deleted = await self.users_repository.delete(user_id)
        print(f'User deleted in service')
        return user_deleted
