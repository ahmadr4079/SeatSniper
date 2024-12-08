from rest_framework.status import HTTP_400_BAD_REQUEST

from seas.app.helpers.exceptions.rest_exceptions.base_rest_exception import BaseRestException


class OtpCodeExpiredRestBadRequest(BaseRestException):
    status_code = HTTP_400_BAD_REQUEST

    def __init__(self):
        super().__init__(message="otp code expired", code="errorOtpCodeExpiredBadRequest")


class NounceCodeExpiredRestBadRequest(BaseRestException):
    status_code = HTTP_400_BAD_REQUEST

    def __init__(self):
        super().__init__(message="nounce code expired", code="errorNounceCodeExpiredBadRequest")


class OtpCodeNotExpireRestBadRequest(BaseRestException):
    status_code = HTTP_400_BAD_REQUEST

    def __init__(self):
        super().__init__(message="otp code not expire", code="errorOtpCodeNotExpireBadRequest")


class OtpCodeNotVerifiedRestBadRequest(BaseRestException):
    status_code = HTTP_400_BAD_REQUEST

    def __init__(self):
        super().__init__(message="otp code not verified", code="errorOtpCodeNotVerifiedBadRequest")


class MaxOtpAttemptsReachedRestBadRequest(BaseRestException):
    status_code = HTTP_400_BAD_REQUEST

    def __init__(self):
        super().__init__(message="maximum otp attempts reached", code="MaxOtpAttemptsReachedBadRequest")
