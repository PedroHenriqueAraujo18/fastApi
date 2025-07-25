from pydantic import BaseModel, EmailStr, ConfigDict


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserDB(UserSchema):
    id: int


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes = True)


class UserList(BaseModel):
    users: list[UserPublic]


class WineSchema(BaseModel):
    name: str
    price: float
    wine_type: str


class WineDB(WineSchema):
    id: int


class WineList(BaseModel):
    wines: list[WineSchema]
