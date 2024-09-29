from pydantic import BaseModel


class UserBaseSchema(BaseModel):
    username: str


class UserCreateSchema(UserBaseSchema):
    password: str


class UserPublicSchema(UserBaseSchema):
    id: int


class UserDBSchema(UserBaseSchema):
    hashed_password: str
