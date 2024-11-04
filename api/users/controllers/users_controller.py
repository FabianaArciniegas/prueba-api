from typing import Annotated
from fastapi import APIRouter, Request, Response, Depends

from api.users.schemas.inputs import UserInput, PatchUserInput, UserBasic, ChangePasswordUserInput
from api.users.services.users_services import UsersService
from core.api_response import ApiResponse
from core.auth import get_current_user
from models.response_model import ResponseModel
from models.users import UsersModel, TokenData
from utils.response_handler import response_handler

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
        api_response: Annotated[ApiResponse, Depends(ApiResponse)]
) -> ResponseModel[UserBasic]:
    api_response.logger.info('Creating user in controller')
    user_service = UsersService(request.app.database, api_response)
    user_created = await user_service.create_user(user_input)
    api_response.logger.info(f'User created in controller')
    return user_created


@users_router.get(
    path="/verify-email/",
    tags=["users"],
    description="Verify email address",
)
@response_handler()
async def verify_email(
        request: Request,
        response: Response,
        id: str,
        token:str,
        api_response: Annotated[ApiResponse, Depends(ApiResponse)]
) -> ResponseModel:
    api_response.logger.info('Verifying email address')
    user_service = UsersService(request.app.database, api_response)
    await user_service.verify_email(id, token)
    return


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
        token_data: Annotated[TokenData, Depends(get_current_user)],
        api_response: Annotated[ApiResponse, Depends(ApiResponse)]
) -> ResponseModel[UserBasic]:
    api_response.logger.info('Getting user in controller')
    user_service = UsersService(request.app.database, api_response, token_data)
    user_found = await user_service.get_user_by_id(user_id)
    api_response.logger.info(f'User found in controller')
    return user_found


@users_router.get(
    path="",
    tags=["users"],
    description="Get all users",
)
@response_handler()
async def get_all_users(
        request: Request,
        response: Response,
        token_data: Annotated[TokenData, Depends(get_current_user)],
        api_response: Annotated[ApiResponse, Depends(ApiResponse)]
) -> ResponseModel[list[UserBasic]]:
    api_response.logger.info('Getting all users in controller')
    user_service = UsersService(request.app.database, api_response)
    all_users = await user_service.get_all_users()
    api_response.logger.info(f'All users found in controller')
    return all_users


@users_router.patch(
    path="/{user_id}",
    tags=["users"],
    description="Update user data",
)
@response_handler()
async def update_user(
        request: Request,
        response: Response,
        user_id: str,
        update_data: PatchUserInput,
        token_data: Annotated[TokenData, Depends(get_current_user)],
        api_response: Annotated[ApiResponse, Depends(ApiResponse)]
) -> ResponseModel[UserBasic]:
    api_response.logger.info('Updating user data in controller')
    user_service = UsersService(request.app.database, api_response, token_data)
    user_updated = await user_service.update_user(user_id, update_data)
    api_response.logger.info(f'User updated some data in controller')
    return user_updated


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
        token_data: Annotated[TokenData, Depends(get_current_user)],
        api_response: ApiResponse = Depends(ApiResponse)
) -> ResponseModel:
    api_response.logger.info('Disabling user in controller')
    user_service = UsersService(request.app.database, api_response, token_data)
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
        token_data: Annotated[TokenData, Depends(get_current_user)],
        api_response: Annotated[ApiResponse, Depends(ApiResponse)]
) -> ResponseModel:
    api_response.logger.info('Deleting user in controller')
    user_service = UsersService(request.app.database, api_response, token_data)
    await user_service.delete_user(user_id)
    api_response.logger.info(f'User deleted in controller')
    return


@users_router.patch(
    path="/change-password/{user_id}",
    tags=["users"],
    description="Update password",
)
@response_handler()
async def change_password(
        request: Request,
        response: Response,
        user_id: str,
        password_data: ChangePasswordUserInput,
        token_data: Annotated[TokenData, Depends(get_current_user)],
        api_response: Annotated[ApiResponse, Depends(ApiResponse)]
) -> ResponseModel[UserBasic]:
    api_response.logger.info('Updating password in controller')
    user_service = UsersService(request.app.database, api_response, token_data)
    changed_password = await user_service.change_password(user_id, password_data)
    api_response.logger.info(f'Password updated in controller')
    return changed_password
