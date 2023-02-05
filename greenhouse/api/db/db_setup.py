from starlette.config import Config

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add env.py file with your local database_url
from .env import DATABASE_URL

# config = Config('.env')
# DATABASE_URL = config('DATABASE_URL')

engine = create_engine(DATABASE_URL, connect_args={}, future=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()