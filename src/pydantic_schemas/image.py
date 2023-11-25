from pydantic import BaseModel
from pydantic import HttpUrl


class Image(BaseModel):
    message: HttpUrl
    status: str
