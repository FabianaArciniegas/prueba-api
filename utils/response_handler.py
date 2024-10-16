import functools

from fastapi import Request, Response

from core.errors import InvalidParameterError, NotFoundError, ForbiddenError, UnauthorizedError, UnexpectedError
from models.response_model import LocationError


def response_handler():
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(request: Request, response: Response, *args, **kwargs):
            api_response = kwargs.get('api_response')
            try:
                result = await func(request, response, *args, **kwargs)
                if result:
                    api_response.data = result
            except InvalidParameterError as error:
                api_response.status = error.status
                api_response.add_error(error)
                api_response.logger.error(error)
            except NotFoundError as error:
                api_response.status = error.status
                api_response.add_error(error)
                api_response.logger.error(error)
            except UnauthorizedError as error:
                api_response.status = error.status
                api_response.add_error(error)
                api_response.logger.error(error)
            except ForbiddenError as error:
                api_response.status = error.status
                api_response.add_error(error)
                api_response.logger.error(error)
            except Exception as error:
                unexpected_error = UnexpectedError(message=error.__str__(), location=LocationError.Server)
                api_response.status = unexpected_error.status
                api_response.add_error(unexpected_error)
                api_response.logger.error(unexpected_error)

            response.status_code = api_response.status.code
            return api_response.set_result

        return wrapper

    return decorator
