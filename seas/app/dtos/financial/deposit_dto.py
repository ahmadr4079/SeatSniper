from pydantic import BaseModel


class ShaparakRedirectDto(BaseModel):
    redirect_url: str
