from functools import wraps

from seas.app.helpers.exceptions.logic_exceptions.customer.otp_logic_exceptions import (
    MaxOtpAttemptsReached,
    NounceCodeExpired,
    OtpCodeExpired,
    OtpCodeNotExpire,
)
from seas.app.helpers.exceptions.rest_exceptions.customer.otp_rest_exceptions import (
    MaxOtpAttemptsReachedRestBadRequest,
    NounceCodeExpiredRestBadRequest,
    OtpCodeExpiredRestBadRequest,
    OtpCodeNotExpireRestBadRequest,
)


def otp_logic_error_handling(function):
    @wraps(function)
    def check_exceptions(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except OtpCodeExpired:
            raise OtpCodeExpiredRestBadRequest
        except NounceCodeExpired:
            raise NounceCodeExpiredRestBadRequest
        except OtpCodeNotExpire:
            raise OtpCodeNotExpireRestBadRequest
        except MaxOtpAttemptsReached:
            raise MaxOtpAttemptsReachedRestBadRequest

    return check_exceptions
