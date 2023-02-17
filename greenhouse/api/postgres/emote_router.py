from os import stat
from typing import Optional, List
import fastapi
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from utilities.emotes import get_emote, get_emotes, get_emote_by_name, create_emote
from db.db_setup import get_db
from pydantic_schemas.emotes import Emote, EmoteCreate

router = fastapi.APIRouter()

# Get batch of emotes
@router.get("/emotes", response_model=List[Emote])
async def read_emotes(skip: int=0, limit: int=100, db:Session = Depends(get_db)):
    emotes = get_emotes(db, skip=skip, limit=limit)
    return emotes

@router.get("/emotes/{id}", response_model=Emote)
async def read_emote(emote_id: int, db: Session = Depends(get_db)):
    emote = get_emote(db, emote_id = emote_id)
    return emote

@router.post("/emotes", response_model=Emote, status_code=201)
async def create_new_emote(emote: EmoteCreate, db: Session = Depends(get_db)):
    db_emote = get_emote_by_name(db=db, emote_name=emote.name)
    if db_emote:
        raise HTTPException(status_code=400, detail="This name is already taken")
    return create_emote(db=db, emote=emote)