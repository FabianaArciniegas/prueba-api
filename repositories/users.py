from core.api_response import ApiResponse
from core.errors import InvalidParameterError, InvalidCredentialsError
from models.response_model import LocationError
from models.users import UsersModel
from repositories.base_repository import BaseRepository, DBModel


class UsersRepository(BaseRepository[UsersModel]):
    _entity_model = UsersModel

    def __init__(self, db, api_response: ApiResponse):
        super().__init__(db, api_response)
        self.api_response = api_response

    async def check_if_the_username_exists(self, username: str) -> None:
        user_found = await self.collection.find_one({'username': username})
        if user_found:
            raise InvalidParameterError(message="There is already a user with that username",
                                        location=LocationError.Body)

    async def get_user_by_username(self, username: str, raise_exception: bool = True) -> DBModel:
        user_found = await self.collection.find_one({'username': username, "is_deleted": False})
        if not user_found and raise_exception:
            raise InvalidCredentialsError(message="Incorrect username or password", location=LocationError.Body)
        return self._entity_model.model_validate(user_found)
