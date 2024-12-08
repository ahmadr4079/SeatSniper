from typing import Optional

from pydantic import BaseModel


class TokenDto(BaseModel):
    access_token: str
    refresh_token: Optional[str]
    expires_in: int
