from pydantic import BaseModel

class Message(BaseModel):
    message: str

class UserSchema(BaseModel):
    username : str
    email : str
    password : str

class WineSchema(BaseModel):
    name : str
    price : float
    wine_type : str
