from fastapi import APIRouter, Request, Response
from fastapi.params import Depends

from api.users.schemas.inputs import UserInput, PatchUserInput, UserBasic
from api.users.services.users_services import UsersService
from core.api_response import ApiResponse
from utils.response_handler import response_handler
from models.response_model import ResponseModel
from models.users import UsersModel

users_router: APIRouter = APIRouter(prefix="/users")


@users_router.post(
    path="",
    tags=["users"],
    description="Create a new user",
)
@response_handler()
async def create_user(
        request: Request,
        response: Response,
        user_input: UserInput,
        api_response: ApiResponse = Depends(ApiResponse)
) -> ResponseModel[UserBasic]:
    api_response.logger.info('Creating user in controller')
    user_service = UsersService(request.app.database, api_response)

    user_created = await user_service.create_user(user_input)
    api_response.logger.info(f'User created in controller')
    return user_created


@users_router.get(
    path="/{user_id}",
    tags=["users"],
    description="Get user by id",
)
@response_handler()
async def get_user_by_id(
        request: Request,
        response: Response,
        user_id: str,
        api_response: ApiResponse = Depends(ApiResponse)
) -> ResponseModel[UsersModel]:
    api_response.logger.info('Getting user in controller')
    user_service = UsersService(request.app.database, api_response)

    user_found = await user_service.get_user_by_id(user_id)
    api_response.logger.info(f'User found in controller')
    return user_found


@users_router.get(
    path="/all/",
    tags=["users"],
    description="Get all users",
)
@response_handler()
async def get_all_users(
        request: Request,
        response: Response,
        api_response: ApiResponse = Depends(ApiResponse)
) -> ResponseModel[list[UsersModel]]:
    api_response.logger.info('Getting all users in controller')
    user_service = UsersService(request.app.database, api_response)

    all_users = await user_service.get_all_users()
    api_response.logger.info(f'All users found in controller')
    return all_users


@users_router.patch(
    path="/update/{user_id}",
    tags=["users"],
    description="Update some user data",
)
@response_handler()
async def update_user(
        request: Request,
        response: Response,
        user_id: str,
        update_data: PatchUserInput,
        api_response: ApiResponse = Depends(ApiResponse)
) -> ResponseModel[UsersModel]:
    api_response.logger.info('Updating some user data in controller')
    user_service = UsersService(request.app.database, api_response)

    user_updated = await user_service.update_user(user_id, update_data)
    api_response.logger.info(f'User updated some data in controller')
    return user_updated


@users_router.put(
    path="/update-all/{user_id}",
    tags=["users"],
    description="Update all user",
)
@response_handler()
async def update_all_user(
        request: Request,
        response: Response,
        user_id: str,
        user_data: UserBasic,
        api_response: ApiResponse = Depends(ApiResponse)
) -> ResponseModel[UsersModel]:
    api_response.logger.info('Updating all user in controller')
    user_service = UsersService(request.app.database, api_response)

    user_all_updated = await user_service.update_all_user(user_id, user_data)
    api_response.logger.info(f'User all updated in controller')
    return user_all_updated


@users_router.patch(
    path="/disable/{user_id}",
    tags=["users"],
    description="Disable user",
)
@response_handler()
async def disable_user(
        request: Request,
        response: Response,
        user_id: str,
        api_response: ApiResponse = Depends(ApiResponse)
) -> ResponseModel:
    api_response.logger.info('Disabling user in controller')
    user_service = UsersService(request.app.database, api_response)

    await user_service.disable_user(user_id)
    api_response.logger.info(f'User disabled in controller')
    return


@users_router.delete(
    path="/delete/{user_id}",
    tags=["users"],
    description="Delete user",
)
@response_handler()
async def delete_user(
        request: Request,
        response: Response,
        user_id: str,
        api_response: ApiResponse = Depends(ApiResponse)
) -> ResponseModel:
    api_response.logger.info('Deleting user in controller')
    user_service = UsersService(request.app.database, api_response)

    await user_service.delete_user(user_id)
    api_response.logger.info(f'User deleted in controller')
    return
