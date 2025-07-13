from pydantic import BaseModel


class UserCreateRequest(BaseModel):
    login: str