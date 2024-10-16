from core.api_response import ApiResponse
from core.errors import InvalidParameterError
from models.response_model import LocationError
from models.users import UsersModel
from repositories.base_repository import BaseRepository


class UsersRepository(BaseRepository[UsersModel]):
    _entity_model = UsersModel

    def __init__(self, db, api_response: ApiResponse):
        super().__init__(db, api_response)
        self.api_response = api_response

    async def check_if_the_user_exists(self, username: str) -> None:
        user_found = await self.collection.find_one({'username': username})
        if user_found:
            raise InvalidParameterError(message="There is already a user with that username",
                                        location=LocationError.Body)
