from fastapi import Request
from fastapi.responses import JSONResponse

from core.api_response import ApiResponse
from core.errors import UnauthorizedError, InvalidParameterError


async def auth_validation_error_handler(request: Request, exception: UnauthorizedError):
    api_response = ApiResponse()
    api_response.status = exception.status
    api_response.add_error(exception)
    api_response.logger.error(exception)
    return JSONResponse(content=api_response.set_result, status_code=exception.status.code)

async def invalid_password_error_handler(request: Request, exception: InvalidParameterError):
    api_response = ApiResponse()
    api_response.status = exception.status
    api_response.add_error(exception)
    api_response.logger.error(exception)
    return JSONResponse(content=api_response.set_result, status_code=exception.status.code)



# async def jwt_error_handler(request: Request, exception: JWTError):
#     api_response = ApiResponse()
#     api_response.status = Status.UNAUTHORIZED
#     api_response.add_error(UnauthorizedError(message="Invalid token or signature verification failed",
#                                              location=LocationError.Headers))
#     api_response.logger.error(exception)
#     return JSONResponse(content=api_response.set_result)


# async def expired_signature_error_handler(request: Request, exception: ExpiredSignatureError):
#     api_response = ApiResponse()
#     api_response.status = Status.UNAUTHORIZED
#     api_response.add_error(UnauthorizedError(message="Token has expired", location=LocationError.Headers))
#     api_response.logger.error(exception)
#     return JSONResponse(content=api_response.set_result)


app_exception_handlers = {
    UnauthorizedError: auth_validation_error_handler,
    InvalidParameterError: invalid_password_error_handler,
    # JWTError: jwt_error_handler,
    # ExpiredSignatureError: expired_signature_error_handler,
}
