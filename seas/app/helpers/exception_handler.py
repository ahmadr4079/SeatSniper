from rest_framework.exceptions import APIException
from rest_framework.response import Response

from seas.app.vos.common_vo import CommonVo


class ExceptionHandler:

    @staticmethod
    def get_exception_dict(code: int, error: str, message: str) -> dict:
        return {CommonVo.code: code, CommonVo.error: error, CommonVo.message: message}

    @staticmethod
    def exception_handler(exc, context) -> Response:
        if isinstance(exc, APIException):
            if isinstance(exc.detail, (list, dict)):
                response_data = ExceptionHandler.get_exception_dict(
                    code=exc.status_code, error=CommonVo.error_validation, message=exc.detail
                )
            else:
                response_data = ExceptionHandler.get_exception_dict(
                    code=exc.status_code, error=exc.detail.code, message=str(exc.detail)
                )
            return Response(response_data, status=exc.status_code)
        if isinstance(exc, Exception):
            print(exc)
            response_data = ExceptionHandler.get_exception_dict(
                code=APIException.status_code, error=APIException.default_code, message=APIException.default_detail
            )
            return Response(response_data, status=APIException.status_code)


exception_handler = ExceptionHandler.exception_handler
