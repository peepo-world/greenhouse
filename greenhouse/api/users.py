from os import stat
from typing import Optional, List
import fastapi
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from utilities.users import get_user, get_users, create_user, get_user_by_email
from db.db_setup import get_db, engine, SessionLocal
from pydantic_schemas.users import User, UserCreate

router = fastapi.APIRouter()

@router.get("/users", response_model=List[User])
async def read_users(skip: int=0, limit: int=100, db: Session = Depends(get_db)):
    users = get_users(db, skip=skip, limit=limit)
    return users

@router.get("/users/{id}", response_model = User)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db=db, user_id=user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/users", response_model=User, status_code=201)
async def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db=db, user_email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="This email has already been registered.")
    print(user)
    return create_user(db=db, user=user)
