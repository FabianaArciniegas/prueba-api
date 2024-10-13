from models.users import UsersModel
from repositories.base_repository import BaseRepository


class UsersRepository(BaseRepository[UsersModel]):
    _entity_model = UsersModel

    async def check_if_the_user_exists(self, username: str) -> None:
        user_found = await self.collection.find_one({'username': username})
        if user_found:
            raise ValueError("There is already a user with that username")
