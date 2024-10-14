from fastapi import APIRouter, Request, Response, HTTPException
from logger_uuid import Logger

from api.users.schemas.inputs import UserInput, PatchUserInput, UserBasic
from api.users.services.users_services import UsersService
from core.errors import InvalidParameterError
from core.response import response_handler
from models.response_model import ResponseModel, StatusCode, LocationError
from models.users import UsersModel

users_router: APIRouter = APIRouter(prefix="/users")


@users_router.post(
    path="",
    tags=["users"],
    description="Create a new user",
)
@response_handler(status_code=StatusCode.OK)
async def create_user(
        request: Request,
        response: Response,
        user_input: UserInput
) -> ResponseModel[UserBasic]:
    logger = Logger()
    logger.log_info('Creating user in controller')
    user_service = UsersService(request.app.database)

    user_created = await user_service.create_user(user_input)
    logger.log_info(f'User created in controller')
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
        user_id: str
) -> ResponseModel[UsersModel]:
    print('Getting user in controller')
    user_service = UsersService(request.app.database)
    user_found = await user_service.get_user_by_id(user_id)
    print(f'User found in controller')
    return user_found

#
# @users_router.get(
#     path="/all/",
#     tags=["users"],
#     description="Get all users"
# )
# async def get_all_users(
#         request: Request,
#         response: Response
# ) -> list[UsersModel]:
#     print('Getting all users in controller')
#     user_service = UsersService(request.app.database)
#     try:
#         all_users = await user_service.get_all_users()
#     except ValueError as e:
#         raise HTTPException(status_code=404, detail=str(e))
#     print(f'All users found in controller')
#     return all_users
#
#
# @users_router.patch(
#     path="/update/{user_id}",
#     tags=["users"],
#     description="Update some user data",
# )
# async def update_user(
#         request: Request,
#         response: Response,
#         user_id: str,
#         update_data: PatchUserInput
# ) -> UsersModel:
#     print('Updating some user data in controller')
#     user_service = UsersService(request.app.database)
#     try:
#         user_updated = await user_service.update_user(user_id, update_data)
#     except ValueError as e:
#         raise HTTPException(status_code=404, detail=str(e))
#     print(f'User updated some data in controller: {user_updated}')
#     return user_updated
#
#
# @users_router.put(
#     path="/updateall/{user_id}",
#     tags=["users"],
#     description="Update all user",
# )
# async def update_all_user(
#         request: Request,
#         response: Response,
#         user_id: str,
#         user_data: UserBasic
# ) -> UsersModel:
#     print('Updating all user in controller')
#     user_service = UsersService(request.app.database)
#     try:
#         user_all_updated = await user_service.update_all_user(user_id, user_data)
#     except ValueError as e:
#         raise HTTPException(status_code=404, detail=str(e))
#     print(f'User all updated in controller: {user_all_updated}')
#     return user_all_updated
#
#
# @users_router.patch(
#     path="/disable/{user_id}",
#     tags=["users"],
#     description="Disable user",
# )
# async def disable_user(
#         request: Request,
#         response: Response,
#         user_id: str
# ) -> UsersModel:
#     print('Disabling user in controller')
#     user_service = UsersService(request.app.database)
#     try:
#         user_disabled = await user_service.disable_user(user_id)
#     except ValueError as e:
#         raise HTTPException(status_code=404, detail=str(e))
#     print(f'User disabled in controller: {user_disabled}')
#     return user_disabled
#
#
# @users_router.delete(
#     path="/delete/{user_id}",
#     tags=["users"],
#     description="Delete user",
# )
# async def delete_user(
#         request: Request,
#         response: Response,
#         user_id: str
# ):
#     print('Deleting user in controller')
#     user_service = UsersService(request.app.database)
#     try:
#         user_deleted = await user_service.delete_user(user_id)
#     except ValueError as e:
#         raise HTTPException(status_code=404, detail=str(e))
#     print(f'User deleted in controller: {user_deleted}')
#     return user_deleted
