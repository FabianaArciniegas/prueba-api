from enum import Enum
from typing import Any, TypeVar, Generic, Type

from pydantic import BaseModel
from starlette import status

DataType = TypeVar('DataType', bound=BaseModel)


class LocationError(str, Enum):
    BODY = "request.body"
    PARAMS = "request.params"


class StatusCode(str, Enum):
    OK = "OK"
    CREATED = "CREATED"
    UNEXPECTED = "UNEXPECTED"
    NOT_FOUND = "NOT_FOUND"


class BaseErrorModel(BaseModel):
    description: str
    message: str
    location: LocationError


class ResponseModel(BaseModel, Generic[DataType]):
    status: str
    data: DataType | None = None
    errors: BaseErrorModel | None = None
