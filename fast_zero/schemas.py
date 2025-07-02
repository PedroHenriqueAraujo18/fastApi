from pydantic import BaseModel,EmailStr

class Message(BaseModel):
    message: str

class UserSchema(BaseModel):
    username : str
    email : EmailStr
    password : str

class UserDB(BaseModel):
    id:int
class UserPublic(BaseModel):
    id: int
    username:str
    email:EmailStr
class WineSchema(BaseModel):
    name : str
    price : float
    wine_type : str
