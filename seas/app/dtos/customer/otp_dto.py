from pydantic import BaseModel


class OtpDto(BaseModel):
    nounce_code: str
    nounce_code_expires_in: float
    otp_code_expires_in: float
