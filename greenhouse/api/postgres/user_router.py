from os import stat
from typing import Optional, List
import fastapi
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from utilities.users import get_user, get_users, create_user, get_user_by_email, get_user_by_name
from db.db_setup import get_db, engine, SessionLocal
from pydantic_schemas.users import User, UserCreate

router = fastapi.APIRouter()

# Get list of users objects in batch of 100
@router.get("/users", response_model=List[User])
async def read_users(skip: int=0, limit: int=100, db: Session = Depends(get_db)):
    users = get_users(db, skip=skip, limit=limit)
    return users

# Get user by id or username.
@router.get("/users/user", response_model = User)
async def read_user(user_id: int=None, user_name: str=None, db: Session = Depends(get_db)):
    if user_id:
        user = get_user(db=db, user_id=user_id)

    if user_name:
        user = get_user_by_name(db=db, user_name=user_name)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

###### Replaced with parameterized query. Probably can get rid of these. ########
# # Get user object by db id
# @router.get("/users/{id}", response_model = User)
# async def read_user(user_id: int, db: Session = Depends(get_db)):
#     user = get_user(db=db, user_id=user_id)

#     if user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user

# # Get user object by username
# @router.get("/users/name/{user_name}", response_model = User)
# async def read_user_name(user_name: str, db: Session = Depends(get_db)):
#     user = get_user_by_name(db=db, user_name=user_name)

#     if user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user

# Create a new user object in db
@router.post("/users", response_model=User, status_code=201)
async def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db=db, user_email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="This email has already been registered.")
    print(user)
    return create_user(db=db, user=user)
