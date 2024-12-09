from enum import StrEnum
from typing import List

from pydantic import Field, PostgresDsn, RedisDsn

from pydantic_settings import BaseSettings


class RunEnvType(StrEnum):
    development = "development"
    stage = "stage"
    production = "production"


class SEASConfig(BaseSettings):
    run_env_type: RunEnvType = Field(default=RunEnvType.development)
    secret_key: str = Field(default="seas-default-secret-key")
    debug: bool = Field(default=False)
    allowed_host: List[str] = ["localhost", "0.0.0.0"]
    pg_dsn: PostgresDsn = 'postgres://postgres:postgres@localhost:5432/seatsniper'
    redis_dsn: RedisDsn = Field('redis://localhost:6379/1')
    otp_code_ttl: int = Field(default=60 * 5)
    nounce_code_ttl: int = Field(default=60 * 15)
    otp_attempt_time_limit_ttl: int = Field(default=60 * 2)
    otp_time_limit_max_attempt: int = Field(default=5)
    access_token_lifetime_minutes: int = Field(default=60)
    refresh_token_lifetime_minutes: int = Field(default=120)

    class Config:
        env_file = '.env'


seas_config = SEASConfig()
