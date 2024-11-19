from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    firstname: str
    lastname: str
    email: str

class UserLogin(BaseModel):
    username:str
    password:str

class UserSchema(UserBase,UserLogin):
    pass