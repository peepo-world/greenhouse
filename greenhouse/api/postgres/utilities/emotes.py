from sqlalchemy.orm import Session
from minio import Minio

from db import models
from pydantic_schemas import emotes

def get_emote(db:Session, emote_id:int):
    return db.query(models.Emote).filter(models.Emote.id == emote_id).first()

def get_emote_by_name(db:Session, emote_name):
    return db.query(models.Emote).filter(models.Emote.name == emote_name).first()

def get_emotes(db:Session, skip:int=0, limit=25):
    return db.query(models.Emote).offset(skip).limit(limit).all()

def create_emote(db:Session, emote:emotes.Emote):
    # Add emote to postgres db
    db_emote = models.Emote(owner_id=emote.owner_id, access=emote.access, name=emote.name, object_name=emote.object_name)
    db.add(db_emote)
    db.commit()
    db.refresh(db_emote)

    return db_emote
    # Add emote to object store
    # put_object(client=client, bucket_name="emotes", object_name=emote.object_name, object=emote.object)