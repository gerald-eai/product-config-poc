from pydantic import BaseModel


class RequestAll(BaseModel):
    skip: int = 0
    limit: int = 100
