from fastapi import APIRouter, Request, Response, HTTPException

from api.users.schemas.inputs import UserInput, PatchUserInput, UserBasic
from api.users.services.users_services import UsersService
from models.users import UsersModel

users_router: APIRouter = APIRouter(prefix="/users")


@users_router.post(
    path="",
    tags=["users"],
    description="Create a new user",
)
async def create_user(
        request: Request,
        response: Response,
        user_input: UserInput
) -> UserBasic:
    print('Creating user in controller')
    user_service = UsersService(request.app.database)
    try:
        user_created = await user_service.create_user(user_input)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    print(f'User created in controller: {user_created}')
    return user_created


@users_router.get(
    path="/username/{username}",
    tags=["users"],
    description="Get user by username",
)
async def get_user_by_username(
        request: Request,
        response: Response,
        username: str
) -> UsersModel:
    print('Getting user by username in controller')
    user_service = UsersService(request.app.database)
    try:
        user_found = await user_service.get_user_by_username(username)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    print(f'User found by username in controller: {user_found}')
    return user_found


@users_router.get(
    path="/id/{user_id}",
    tags=["users"],
    description="Get user by id",
)
async def get_user_by_id(
        request: Request,
        response: Response,
        user_id: str
) -> UsersModel:
    print('Getting user by id in controller')
    user_service = UsersService(request.app.database)
    try:
        user_found = await user_service.get_user_by_id(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    print(f'User found by id in controller: {user_found}')
    return user_found


@users_router.get(
    path="/all/",
    tags=["users"],
    description="Get all users"
)
async def get_all_users(
        request: Request,
        response: Response
) -> list[UsersModel]:
    print('Getting all users in controller')
    user_service = UsersService(request.app.database)
    try:
        all_users = await user_service.get_all_users()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    print(f'All users found in controller: {all_users}')
    return all_users


@users_router.patch(
    path="/update/{user_id}",
    tags=["users"],
    description="Update some user data by id",
)
async def update_user(
        request: Request,
        response: Response,
        user_id: str,
        update_data: PatchUserInput
) -> UsersModel:
    print('Updating some user data by id in controller')
    user_service = UsersService(request.app.database)
    try:
        user_updated = await user_service.update_user(user_id, update_data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    print(f'User updated some data by id in controller: {user_updated}')
    return user_updated


@users_router.put(
    path="/updateall/{user_id}",
    tags=["users"],
    description="Update all user by id",
)
async def update_all_user(
        request: Request,
        response: Response,
        user_id: str,
        update_all_user: UserBasic
) -> UsersModel:
    print('Updating all user by id in controller')
    user_service = UsersService(request.app.database)
    try:
        user_all_updated = await user_service.update_all_user(user_id, update_all_user)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    print(f'User all updated by id in controller: {user_all_updated}')
    return user_all_updated


@users_router.patch(
    path="/isdeleted/{user_id}",
    tags=["users"],
    description="Deactivate user by id",
)
async def deactivate_user(
        request: Request,
        response: Response,
        user_id: str
) -> UsersModel:
    print('Deactivating user by id in controller')
    user_service = UsersService(request.app.database)
    try:
        user_disabled = await user_service.deactivate_user(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    print(f'User disabled by id in controller: {user_disabled}')
    return user_disabled


@users_router.delete(
    path="/delete/{user_id}",
    tags=["users"],
    description="Delete user by id",
)
async def delete_user(
        request: Request,
        response: Response,
        user_id: str
):
    print('Deleting user by id in controller')
    user_service = UsersService(request.app.database)
    try:
        user_deleted = await user_service.delete_user(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    print(f'User deleted by id in controller: {user_deleted}')
    return user_deleted
