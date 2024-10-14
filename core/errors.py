from fastapi import HTTPException


class InvalidParameterError(HTTPException):
    status_code = 401

    def __init__(self, detail: str):
        self.detail = detail
        super(InvalidParameterError, self).__init__(self.status_code, detail=self.detail)
