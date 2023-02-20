from pydantic import BaseModel

class EmoteBase(BaseModel):
    owner_id: int
    access: bool
    name: str
    command: str

class EmoteCreate(EmoteBase):
    object_name: str
    

class Emote(EmoteBase):
    name: str
    

    class Config:
        orm_mode = True