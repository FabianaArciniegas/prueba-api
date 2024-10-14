from functools import wraps

from starlette import status

from models.response_model import ResponseModel, StatusCode


def response_handler(status_code: str = StatusCode.OK):
    def wraps_function(function):
        @wraps(function)
        async def wrapper(*args, **kwargs):
            result = await function(*args, **kwargs)
            return ResponseModel(status_code=status_code, data=result)

        return wrapper

    return wraps_function
