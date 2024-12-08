from drf_spectacular.utils import OpenApiExample
from rest_framework.exceptions import APIException

from seas.app.helpers.exception_handler import ExceptionHandler


class BaseRestException(APIException):
    def __init__(self, message: str, code: str):
        super().__init__(detail=message, code=code)

    @property
    def openapi_example(self):
        code: int = self.status_code
        error = self.detail.code
        message = str(self.detail)
        return OpenApiExample(
            name=error,
            value=ExceptionHandler.get_exception_dict(code=code, error=error, message=message),
            response_only=True,
            status_codes=[str(code)],
        )
