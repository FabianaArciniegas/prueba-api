from fastapi import HTTPException

from models.response_model import BaseErrorModel, LocationError


class BaseExceptions(Exception):
    def __init__(self, status_code, description, message, location):
        self.status_code = status_code
        self.description = description
        self.message = message
        self.location = location

    def __str__(self):
        return f"Error: {self.__class__.__name__} - {self.description} - {self.message}"

    def add_error(self):
        return BaseErrorModel(description=self.description, message=self.message, location=self.location)


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
    status_code = 400
    description = "Parameter error"


class UnauthorizedError(_BaseException):
    status_code = 401
    description = "unauthorized error"


class ForbiddenError(_BaseException):
    status_code = 403
    description = "Unauthorized access"


class NotFoundError(_BaseException):
    status_code = 404
    description = "Object not found"
