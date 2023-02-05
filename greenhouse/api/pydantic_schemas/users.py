from typing import List

from pydantic import BaseModel

users = list()

class UserBase(BaseModel):
    user_name:str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    # relationship w/ Profile. Maybe emotes?
    class Config:
        orm_mode = True


