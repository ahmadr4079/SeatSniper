from rest_framework import status
from rest_framework.response import Response


class CommonResponse(Response):
    def __init__(self, message: str):
        response = {"code": status.HTTP_200_OK, "message": message}
        super().__init__(
            data=response,
            status=status.HTTP_200_OK,
        )
