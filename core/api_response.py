from typing import Any
from uuid import uuid4

from core.errors import BaseExceptions
from models.response_model import BaseErrorModel, Status, ResponseModel
from utils.logger import logger_api


class ApiResponse:
    def __init__(self):
        self._process_id = str(uuid4())
        self._status = Status.OK
        self._data = None
        self._errors = []
        self._logger = logger_api(self._process_id)

    def add_error(self, error: BaseExceptions):
        self._errors.append(
            BaseErrorModel(description=error.description, message=error.message, location=error.location))

    @property
    def process_id(self):
        return self._process_id

    @property
    def status(self):
        return self._status

    @property
    def data(self):
        return self._data

    @property
    def errors(self):
        return self._errors

    @property
    def logger(self):
        return self._logger

    @status.setter
    def status(self, value: Status):
        self._status = value

    @data.setter
    def data(self, value: Any):
        self._data = value

    @property
    def set_result(self):
        response = ResponseModel(
            process_id=self._process_id,
            status=self._status.value,
            data=self._data,
            errors=self._errors,
        ).model_dump()
        return response
