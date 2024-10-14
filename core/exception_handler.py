from functools import wraps

from fastapi import Request, Response

from core.errors import InvalidParameterError, NotFoundError, UnexpectedError
from models.response_model import StatusCode, LocationError


def exception_handler(status_code: StatusCode = StatusCode.OK):
    def wraps_function(function):
        @wraps(function)
        async def wrapper(request: Request, response: Response, *args, **kwargs):
            api_response = kwargs.get("api_response")
            api_response.status_code = status_code
            try:
                result = await function(request, response, *args, **kwargs)
                if result:
                    api_response.data = result
            except InvalidParameterError as error:
                api_response.logger.log_error(error)
                api_response.status_code = error.status_code
                api_response.add_error(error)
            except NotFoundError as error:
                api_response.logger.log_error(error)
                api_response.status_code = error.status_code
                api_response.add_error(error)
            except Exception as error:
                unexpected_error = UnexpectedError(message=error.__str__(), location=LocationError.SERVER)
                api_response.logger.log_error(error)
                api_response.status_code = unexpected_error.status_code
                api_response.add_error(unexpected_error)

            response.status_code = api_response.status_code.code
            return api_response.set_result

        return wrapper

    return wraps_function
