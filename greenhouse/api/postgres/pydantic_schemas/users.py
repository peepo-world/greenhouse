from pydantic import BaseModel
from pydantic.schema import Optional


class UserBase(BaseModel):
    user_name: str
    email: str


class UserCreate(UserBase):
    twitch_id: str


class User(UserBase):
    id: int

    # relationship w/ Profile. Maybe emotes?
    class Config:
        orm_mode = True


