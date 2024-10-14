from fastapi import HTTPException

from models.response_model import BaseErrorModel, LocationError, StatusCode


class BaseExceptions(Exception):
    def __init__(self, status_code, description, message, location):
        self.status_code = status_code
        self.description = description
        self.message = message
        self.location = location

    def __str__(self):
        return f"Error: {self.__class__.__name__} - {self.description} - {self.message}"


class _BaseException(BaseExceptions):
    status_code = None
    description = None

    def __init__(self, message: str, location: LocationError):
        self.message = message
        self.location = location
        super().__init__(
            status_code=self.status_code,
            description=self.description,
            message=self.message,
            location=self.location
        )


class InvalidParameterError(_BaseException):
    status_code = StatusCode.BAD_REQUEST
    description = "Parameter error"


class UnauthorizedError(_BaseException):
    status_code = StatusCode.UNAUTHORIZED
    description = "unauthorized error"


class ForbiddenError(_BaseException):
    status_code = StatusCode.FORBIDDEN
    description = "Unauthorized access"


class NotFoundError(_BaseException):
    status_code = StatusCode.NOT_FOUND
    description = "Object not found"


class UnexpectedError(_BaseException):
    status_code = StatusCode.UNEXPECTED
    description = "Unexpected error"
