from models.users import UsersModel
from repositories.base_repository import BaseRepository


class UsersRepository(BaseRepository[UsersModel]):
    _entity_model = UsersModel

    async def create_user(self, user_data: dict) -> UsersModel:
        user_created = await self.create(user_data)
        return user_created

    async def get_user_by_username(self, username: str) -> UsersModel:
        user_found = await self.get("username", username)
        return user_found

    async def get_user_by_id(self, user_id: str) -> UsersModel:
        user_found = await self.get("_id", user_id)
        return user_found

    async def get_all_users(self) -> list[UsersModel]:
        all_users = await self.get_all("is_deleted", False)
        return all_users

    async def update_user(self, user_id: str, update_data: dict) -> UsersModel:
        user_updated = await self.update("_id", user_id, update_data)
        return user_updated

    async def update_all_user(self, user_id: str, update_data: dict) -> UsersModel:
        update_data["_id"] = user_id
        user_updated = await self.update_all("_id", user_id, update_data)
        return user_updated

    async def deactivate_user(self, user_id: str, update_data: dict) -> UsersModel:
        user_deactivated = await self.deactivate("_id", user_id, update_data)
        return user_deactivated

    async def delete_user(self, user_id: str):
        user_deleted = await self.delete("_id", user_id)
        return user_deleted
