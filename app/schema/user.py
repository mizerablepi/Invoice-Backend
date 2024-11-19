from pydantic import BaseModel, ConfigDict

class UserBase(BaseModel):
    username: str
    firstname: str
    lastname: str
    email: str

class UserLogin(BaseModel):
    username:str
    password:str

class UserSchema(UserBase,UserLogin):
    model_config = ConfigDict(from_attributes=True)
    pass