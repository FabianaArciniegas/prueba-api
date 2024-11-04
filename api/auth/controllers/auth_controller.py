from typing import Annotated
from fastapi import APIRouter, Request, Response, Depends
from fastapi.security import OAuth2PasswordRequestForm

from api.auth.schemas.inputs import UserLogin, Token, PasswordRecovery, ResetPasswordUserInput
from api.auth.services.auth_services import AuthServices
from api.users.schemas.inputs import UserBasic
from core.api_response import ApiResponse
from core.auth import get_current_user
from models.response_model import ResponseModel
from models.users import TokenData, TokenResponse
from utils.response_handler import response_handler

auth_router: APIRouter = APIRouter(prefix="/auth")


@auth_router.post(
    path="/login",
    tags=["auth"],
    description="Login user",
)
@response_handler()
async def login_user(
        request: Request,
        response: Response,
        user_login: UserLogin,
        api_response: Annotated[ApiResponse, Depends(ApiResponse)]
) -> ResponseModel[TokenResponse]:
    api_response.logger.info('Login user in controller')
    auth_service = AuthServices(request.app.database, api_response)
    tokens = await auth_service.login_user(user_login)
    api_response.logger.info(f'User logged in controller')
    return tokens


@auth_router.post(
    path="/refresh",
    tags=["auth"],
    description="Refresh access token",
)
@response_handler()
async def refresh_token(
        request: Request,
        response: Response,
        refresh_token_user: Token,
        api_response: Annotated[ApiResponse, Depends(ApiResponse)]
) -> ResponseModel[TokenResponse]:
    api_response.logger.info('Refresh token in controller')
    auth_service = AuthServices(request.app.database, api_response)
    tokens = await auth_service.refresh_token(refresh_token_user.token)
    api_response.logger.info(f'Token refreshed in controller')
    return tokens


@auth_router.post(
    path="/logout",
    tags=["auth"],
    description="Logout user",
)
@response_handler()
async def logout_user(
        request: Request,
        response: Response,
        token_data: Annotated[TokenData, Depends(get_current_user)],
        api_response: Annotated[ApiResponse, Depends(ApiResponse)]
) -> ResponseModel:
    api_response.logger.info('Logging out user in controller')
    auth_service = AuthServices(request.app.database, api_response)
    await auth_service.logout_user(token_data.id)
    api_response.logger.info(f'User logged out in controller')
    return


@auth_router.post(
    path="/token",
    tags=["auth"],
    description="Token user",
    include_in_schema=False
)
@response_handler(raw_response=True)
async def auth_user_token(
        request: Request,
        response: Response,
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        api_response: Annotated[ApiResponse, Depends(ApiResponse)]
) -> dict:
    api_response.logger.info('Authenticate user in controller')
    auth_service = AuthServices(request.app.database, api_response)
    tokens = await auth_service.auth_user_token(form_data)
    api_response.logger.info(f'User authenticated in controller')
    return tokens.model_dump()


@auth_router.post(
    path="/recovery-password",
    tags=["auth"],
    description="Recovery password",
)
@response_handler()
async def forgot_password(
        request: Request,
        response: Response,
        email_user: PasswordRecovery,
        api_response: Annotated[ApiResponse, Depends(ApiResponse)]
) -> ResponseModel:
    api_response.logger.info('Recovery password in controller')
    auth_service = AuthServices(request.app.database, api_response)
    await auth_service.forgot_password(email_user.email)
    api_response.logger.info('Password reset email sent successfully in controller')
    return


@auth_router.post(
    path="/reset-password",
    tags=["auth"],
    description="Reset password",
)
@response_handler()
async def reset_password(
        request: Request,
        response: Response,
        password_data: ResetPasswordUserInput,
        api_response: Annotated[ApiResponse, Depends(ApiResponse)]
) -> ResponseModel[UserBasic]:
    api_response.logger.info('Reset password in controller')
    auth_service = AuthServices(request.app.database, api_response)
    password_updated = await auth_service.reset_password(password_data)
    api_response.logger.info('Password updated in controller')
    return password_updated
