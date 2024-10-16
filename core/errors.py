from models.response_model import LocationError, Status


class BaseExceptions(Exception):
    def __init__(self, status, description, message, location):
        self.status = status
        self.description = description
        self.message = message
        self.location = location

    def __str__(self):
        return f'Error: {self.description} - {self.message} - {self.location}'


class _BaseException(BaseExceptions):
    status = None,
    description = None,

    def __init__(self, message: str, location: LocationError):
        self.message = message
        self.location = location
        super().__init__(
            status=self.status,
            description=self.description,
            message=self.message,
            location=self.location,
        )


class InvalidParameterError(_BaseException):
    status = Status.BAD_REQUEST
    description = "Parameter error"


class UnexpectedError(_BaseException):
    status = Status.UNEXPECTED
    description = "Unexpected error"


class NotFoundError(_BaseException):
    status = Status.NOT_FOUND
    description = "Object not found"


class UnauthorizedError(_BaseException):
    status = Status.UNAUTHORIZED
    description = "unauthorized error"


class ForbiddenError(_BaseException):
    status = Status.FORBIDDEN
    description = "Unauthorized access"
