import uuid

from django.utils.crypto import get_random_string

from seas.app.dtos.customer.otp_dto import OtpDto
from seas.app.helpers.error_handling.customer.otp_logic_error_handling import otp_logic_error_handling
from seas.app.helpers.exceptions.logic_exceptions.customer.otp_logic_exceptions import (
    MaxOtpAttemptsReached,
    NounceCodeExpired,
    OtpCodeExpired,
    OtpCodeNotExpire,
)
from seas.app.helpers.singleton import Singleton
from seas.app.repositories.customer.otp_repository import OtpRepository
from seas.project.config import RunEnvType, seas_config


class OtpLogic(metaclass=Singleton):

    def __init__(self):
        self.otp_repository = OtpRepository()

    def generate_nounce_code(self) -> str:
        return str(uuid.uuid4().hex)

    def generate_otp_code(self) -> int:
        otp_code = get_random_string(length=5, allowed_chars="123456789")
        if seas_config.run_env_type == RunEnvType.development:
            return 11111
        return int(otp_code)

    @otp_logic_error_handling
    def set_otp(self, phone_number: str) -> OtpDto:
        nounce_code = self.otp_repository.get_last_nounce_code_cache(phone_number=phone_number)
        if nounce_code is None:
            nounce_code = self.generate_nounce_code()
            nounce_code_expires_in = self.otp_repository.set_nounce_code_cache(
                phone_number=phone_number, nounce_code=nounce_code
            )
        else:
            nounce_code_expires_in = self.otp_repository.get_nounce_code_expires_in(
                phone_number=phone_number, nounce_code=nounce_code
            )
        otp_code = self.otp_repository.get_last_otp_code_cache(phone_number=phone_number, nounce_code=nounce_code)
        if otp_code is not None:
            raise OtpCodeNotExpire
        otp_code = self.generate_otp_code()
        otp_code_expires_in = self.otp_repository.set_otp_code_cache(
            otp_code=otp_code, nounce_code=nounce_code, phone_number=phone_number
        )
        return OtpDto(
            nounce_code=nounce_code,
            nounce_code_expires_in=nounce_code_expires_in,
            otp_code_expires_in=otp_code_expires_in,
        )

    @otp_logic_error_handling
    def check_otp(self, phone_number: str, nounce_code: str, otp_code: int):
        attempt = self.otp_repository.get_otp_attempt(phone_number=phone_number)
        if attempt < seas_config.otp_time_limit_max_attempt:
            self.otp_repository.set_otp_attempt(phone_number=phone_number, attempt=attempt + 1)
        else:
            raise MaxOtpAttemptsReached
        nounce_code = self.otp_repository.get_nounce_code_cache(phone_number=phone_number, nounce_code=nounce_code)
        if nounce_code is None:
            raise NounceCodeExpired
        otp_code = self.otp_repository.get_otp_code_cache(
            phone_number=phone_number, nounce_code=nounce_code, otp_code=otp_code
        )
        if otp_code is None:
            raise OtpCodeExpired
        self.otp_repository.delete_nounce_code_cache(phone_number=phone_number)
        self.otp_repository.delete_otp_code_cache(phone_number=phone_number)
