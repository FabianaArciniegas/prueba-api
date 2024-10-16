from enum import Enum
from typing import TypeVar, Generic

from pydantic import BaseModel

DataType = TypeVar('DataType', bound=BaseModel)


class Status(Enum):
    OK = "OK", 200
    CREATED = "CREATED", 201
    UNEXPECTED = "UNEXPECTED", 500
    NOT_FOUND = "NOT_FOUND", 404
    BAD_REQUEST = "BAD_REQUEST", 400
    UNAUTHORIZED = "UNAUTHORIZED", 401
    FORBIDDEN = "FORBIDDEN", 403

    def __new__(cls, *args, **kwargs):
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    def __init__(self, _: str, code: int):
        self._code = code

    def __str__(self):
        return self.value

    @property
    def code(self):
        return self._code


class LocationError(str, Enum):
    Body = "request.body"
    Params = "request.params"
    Headers = "request.headers"
    Cookies = "request.cookies"
    Server = "request.server"


class BaseErrorModel(BaseModel):
    description: str
    message: str
    location: LocationError


class ResponseModel(BaseModel, Generic[DataType]):
    process_id: str
    status: str
    data: DataType | list[DataType] | None = None
    errors: list[BaseErrorModel] | None = None
