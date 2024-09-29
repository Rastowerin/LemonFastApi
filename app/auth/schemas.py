from pydantic import BaseModel


class UserCredentialsSchema(BaseModel):
    username: str
    password: str
