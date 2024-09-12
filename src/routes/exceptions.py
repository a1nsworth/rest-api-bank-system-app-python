from fastapi import HTTPException
from starlette import status


class BaseNotFound(HTTPException):
    __message__: str = "not found"
    __status_code__ = status.HTTP_400_BAD_REQUEST

    def __init__(self):
        super().__init__(status_code=self.__status_code__, detail=self.__message__)


class BankNotFoundException(BaseNotFound):
    __message__: str = "bank not found"


class BankOfficeNotFoundException(BaseNotFound):
    __message__: str = "bank office not found"
