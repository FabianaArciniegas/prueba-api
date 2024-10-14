from typing import Any

from logger_uuid import Logger

from core.errors import BaseExceptions
from models.response_model import BaseErrorModel, ResponseModel, StatusCode


class ApiResponse:
    def __init__(self):
        self._status_code = StatusCode.BAD_REQUEST
        self._data = None
        self._errors = []
        self._logger = Logger()

    def add_error(self, error: BaseExceptions):
        self._errors.append(BaseErrorModel(
            description=error.description,
            message=error.message,
            location=error.location
        ))

    @property
    def status_code(self):
        return self._status_code

    @property
    def data(self):
        return self._data

    @property
    def logger(self):
        return self._logger

    @property
    def errors(self):
        return self._errors

    @status_code.setter
    def status_code(self, value: StatusCode):
        self._status_code = value

    @data.setter
    def data(self, value: Any):
        self._data = value

    @property
    def set_result(self):
        response = ResponseModel(
            status=self._status_code.value,
            data=self._data,
            errors=self._errors,
            process_id=self._logger.process_id,
        ).model_dump()
        return response
