from pydantic import BaseModel, ConfigDict


class UserBaseSchema(BaseModel):
    username: str

    model_config = ConfigDict(from_attributes=True)


class UserCreateSchema(UserBaseSchema):
    password: str


class UserPublicSchema(UserBaseSchema):
    id: int


class UserDBSchema(UserBaseSchema):
    hashed_password: str
