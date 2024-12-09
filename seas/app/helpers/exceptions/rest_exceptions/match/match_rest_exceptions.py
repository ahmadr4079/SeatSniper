from rest_framework.status import HTTP_404_NOT_FOUND

from seas.app.helpers.exceptions.rest_exceptions.base_rest_exception import BaseRestException


class MatchRestNotFound(BaseRestException):
    status_code = HTTP_404_NOT_FOUND

    def __init__(self):
        super().__init__(message="match not found", code="errorMatchNotFound")
