from pydantic import BaseModel
from pydantic import HttpUrl


class Images(BaseModel):
    message: list[HttpUrl]
    status: str
