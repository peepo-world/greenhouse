from sqlalchemy.orm import Session

from db import models
from pydantic_schemas import users


def get_user(db:Session, user_id:int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db:Session, user_email:str):
    return db.query(models.User).filter(models.User.email == user_email).first()

def get_user_by_name(db:Session, user_name:str):
    return db.query(models.User).filter(models.User.user_name == user_name).first()

def get_users(db:Session, skip: int=0, limit: int=100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db:Session, user: users.UserCreate):
    db_user = models.User(email=user.email, user_name=user.user_name, twitch_id=user.twitch_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user