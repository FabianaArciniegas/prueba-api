from functools import wraps

from logger_uuid import Logger
from starlette import status

from core.errors import InvalidParameterError, NotFoundError
from models.response_model import ResponseModel, StatusCode, BaseErrorModel


def response_handler(status_code: str = StatusCode.OK):
    def wraps_function(function):
        @wraps(function)
        async def wrapper(*args, **kwargs):
            logger = Logger()
            response = kwargs.get("response")
            try:
                result = await function(*args, **kwargs)
            except InvalidParameterError as e:
                error = e.add_error()
                logger.log_error(e.__str__())
                response.status_code = e.status_code
                return ResponseModel(status=StatusCode.UNEXPECTED, errors=error)
            except NotFoundError as e:
                error = e.add_error()
                logger.log_error(e.__str__())
                response.status_code = e.status_code
                return ResponseModel(status=StatusCode.NOT_FOUND, errors=error)
            except Exception as e:
                return ResponseModel(status=StatusCode.UNEXPECTED)
            return ResponseModel(status_code=status_code, data=result)

        return wrapper

    return wraps_function
