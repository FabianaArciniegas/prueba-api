from datetime import datetime

from motor.motor_asyncio import AsyncIOMotorDatabase

from api.users.schemas.inputs import UserInput, PatchUserInput, UserBasic
from models.users import UsersModel
from repositories.users import UsersRepository


class UsersService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.users_repository = UsersRepository(self.db)

    async def password_hasher(self, raw_password: str):
        return 'secret' + raw_password

    async def create_user(self, user_input: UserInput):
        print('Creating user in service')
        user_found = await self.users_repository.get_user_by_username(user_input.username)
        if user_found:
            raise ValueError('There is already a user with that username')
        hashed_password = await self.password_hasher(user_input.password)
        user_data = user_input.model_dump()
        user_data['hashed_password'] = hashed_password
        user_created = await self.users_repository.create_user(user_data)
        if user_created is None:
            raise ValueError("User not created")
        print(f'User created in service: {user_created}')
        return user_created

    async def get_user_by_username(self, username: str) -> UsersModel:
        print('Getting user by username in service')
        user_found = await self.users_repository.get_user_by_username(username)
        if user_found is None:
            raise ValueError("User not found")
        print(f'User found by username in service: {user_found}')
        return user_found

    async def get_user_by_id(self, user_id: str) -> UsersModel:
        print('Getting user by id in service')
        user_found = await self.users_repository.get_user_by_id(user_id)
        if user_found is None:
            raise ValueError("User not found")
        print(f'User found by id in service: {user_found}')
        return user_found

    async def get_all_users(self) -> list[UsersModel]:
        print('Getting all users in service')
        all_users = await self.users_repository.get_all_users()
        if all_users is None:
            raise ValueError("There are no users")
        print(f'All users found in service: {all_users}')
        return all_users

    async def update_user(self, user_id: str, update_data: PatchUserInput) -> UsersModel:
        print('Updating some user data by id in service')
        user_by_update = await self.users_repository.get_user_by_id(user_id)
        if user_by_update is None:
            raise ValueError("User not found")
        user_updated = await self.users_repository.update_user(user_id, update_data.model_dump())
        if user_updated is None:
            raise ValueError("User not updated")
        print(f'User updated some data by id in service: {user_updated}')
        return user_updated

    async def update_all_user(self, user_id: str, update_user: UserBasic) -> UsersModel:
        print('Updating all user by id in service')
        user = await self.users_repository.get_user_by_id(user_id)
        if user is None:
            raise ValueError("User not found")
        user.update_at = datetime.utcnow()
        user.username = update_user.username
        user.email = update_user.email
        user.full_name = update_user.full_name
        user_all_updated = await self.users_repository.update_all_user(user_id, user.model_dump())
        if user_all_updated is None:
            raise ValueError("User not updated")
        print(f'User all updated by id in service: {user_all_updated}')
        return user_all_updated

    async def deactivate_user(self, user_id: str):
        print('Deactivating user by id in service')
        user_by_deactivate = await self.users_repository.get_user_by_id(user_id)
        if user_by_deactivate is None:
            raise ValueError("User not found")
        user_by_deactivate.is_deleted = True
        user_disabled = await self.users_repository.deactivate_user(user_id, user_by_deactivate.model_dump())
        if user_disabled is None:
            raise ValueError("User not disabled")
        print(f'User disabled by id in service: {user_disabled}')
        return user_disabled

    async def delete_user(self, user_id: str):
        print('Deleting user by id in service')
        user_by_delete = await self.users_repository.get_user_by_id(user_id)
        if user_by_delete is None:
            raise ValueError("User not found")
        user_deleted = await self.users_repository.delete_user(user_id)
        if user_deleted is None:
            raise ValueError("User not deleted")
        print(f'User deleted by id in service: {user_deleted}')
        return user_deleted
