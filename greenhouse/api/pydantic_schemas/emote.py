from pydantic import BaseModel

class EmoteBase(BaseModel):
    owner_id: int
    access: bool


class Emote(EmoteBase):
    name: str