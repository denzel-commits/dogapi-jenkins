from pydantic import BaseModel


class Error(BaseModel):
    status: str
    message: str
    code: int = 404
