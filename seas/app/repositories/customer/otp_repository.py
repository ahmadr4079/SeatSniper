import datetime

from seas.app.adapters.redis_base_adapter import RedisBaseAdapter
from seas.app.helpers.singleton import Singleton
from seas.project.config import seas_config


class OtpRepository(RedisBaseAdapter, metaclass=Singleton):
    OTP_CODE_CACHE = (
        "phone_number:{phone_number}:otp_code:{otp_code}:nounce_code:{nounce_code}",
        seas_config.otp_code_ttl,
    )
    NOUNCE_CODE_CACHE = ("phone_number:{phone_number}:nounce_code:{nounce_code}", seas_config.nounce_code_ttl)
    OTP_SESSION_ATTEMPT = ("otp_attempt:phone_number:{phone_number}", seas_config.otp_attempt_time_limit_ttl)

    def set_otp_attempt(self, phone_number: str, attempt: int):
        key = self.OTP_SESSION_ATTEMPT[0].format(phone_number=phone_number)
        self.client.set(key, attempt, self.OTP_SESSION_ATTEMPT[1])

    def get_otp_attempt(self, phone_number: str) -> int:
        key = self.OTP_SESSION_ATTEMPT[0].format(phone_number=phone_number)
        if (attempt := self.client.get(key)) is not None:
            return int(attempt)
        return 0

    def get_otp_code_cache(self, phone_number: str, nounce_code: str, otp_code: int):
        key = self.OTP_CODE_CACHE[0].format(phone_number=phone_number, nounce_code=nounce_code, otp_code=otp_code)
        return self.client.get(key)

    def set_otp_code_cache(self, phone_number: str, otp_code: int, nounce_code: str):
        key = self.OTP_CODE_CACHE[0].format(phone_number=phone_number, nounce_code=nounce_code, otp_code=otp_code)
        self.client.set(key, otp_code, self.OTP_CODE_CACHE[1])
        return (datetime.datetime.now() + datetime.timedelta(seconds=self.OTP_CODE_CACHE[1])).timestamp()

    def get_nounce_code_cache(self, phone_number: str, nounce_code: str):
        key = self.NOUNCE_CODE_CACHE[0].format(phone_number=phone_number, nounce_code=nounce_code)
        return self.client.get(key)

    def set_nounce_code_cache(self, phone_number: str, nounce_code: str):
        key = self.NOUNCE_CODE_CACHE[0].format(phone_number=phone_number, nounce_code=nounce_code)
        self.client.set(key, nounce_code, ex=self.NOUNCE_CODE_CACHE[1])
        return (datetime.datetime.now() + datetime.timedelta(seconds=self.NOUNCE_CODE_CACHE[1])).timestamp()

    def delete_nounce_code_cache(self, phone_number: str):
        key = self.NOUNCE_CODE_CACHE[0].format(phone_number=phone_number, nounce_code="*")
        specified_keys = self.client.keys(key)
        if specified_keys:
            self.client.delete(*specified_keys)

    def delete_otp_code_cache(self, phone_number: str):
        key = self.OTP_CODE_CACHE[0].format(phone_number=phone_number, otp_code="*", nounce_code="*")
        specified_keys = self.client.keys(key)
        if specified_keys:
            self.client.delete(*specified_keys)

    def get_last_nounce_code_cache(self, phone_number: str):
        key = self.NOUNCE_CODE_CACHE[0].format(phone_number=phone_number, nounce_code="*")
        specified_keys = self.client.keys(key)
        if specified_keys:
            return self.client.get(specified_keys[0])

    def get_last_otp_code_cache(self, phone_number: str, nounce_code: str):
        key = self.OTP_CODE_CACHE[0].format(phone_number=phone_number, nounce_code=nounce_code, otp_code="*")
        specified_keys = self.client.keys(key)
        if specified_keys:
            return self.client.get(specified_keys[0])

    def get_nounce_code_expires_in(self, phone_number: str, nounce_code: str):
        key = self.NOUNCE_CODE_CACHE[0].format(phone_number=phone_number, nounce_code=nounce_code)
        ttl = self.client.ttl(key)
        if ttl is None:
            ttl = 0
        return (datetime.datetime.now() + datetime.timedelta(seconds=ttl)).timestamp()
