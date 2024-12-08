from enum import StrEnum
from typing import List

from pydantic import Field, PostgresDsn

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

    class Config:
        env_file = '.env'


seas_config = SEASConfig()
