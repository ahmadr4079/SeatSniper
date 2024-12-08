from seas.app.helpers.exceptions.logic_exceptions.base_logic_exception import BaseLogicException


class OtpCodeNotExpire(BaseLogicException):
    pass


class NounceCodeExpired(BaseLogicException):
    pass


class OtpCodeExpired(BaseLogicException):
    pass


class MaxOtpAttemptsReached(BaseLogicException):
    pass
