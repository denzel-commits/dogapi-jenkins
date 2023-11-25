from pydantic import BaseModel


class Breeds(BaseModel):
    message: dict
    status: str
