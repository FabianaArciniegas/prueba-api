from enum import Enum
from typing import Any

from pydantic import BaseModel
from starlette import status


class LocationError(str, Enum):
    BODY = "request.body"
    PARAMS = "request.params"


class StatusCode(str, Enum):
    OK = "OK"
    CREATED = "CREATED"


class BaseError(BaseModel):
    description: str
    message: str
    location: LocationError


class ResponseModel(BaseModel):
    status_code: str
    data: Any
    errors: BaseError | None = None
