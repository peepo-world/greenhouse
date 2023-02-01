# SPDX-FileCopyrightText: 2023 peepo.world developers
#
# SPDX-License-Identifier: EUPL-1.2

from starlette.applications import Starlette
from starlette.routing import Route

from sqlalchemy import create_engine, Column, Integer, String, LargeBinary, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from starlette.config import Config
import routes

config = Config('.env')
DATABASE_URL = config('DATABASE_URL')

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread":False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Emote(Base):
    __tablename__ = "emote"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    owner = Column(String)
    access = Column(Boolean)
    image = Column(LargeBinary)



app = Starlette(
    debug=True,
    routes=[
        Route('/', routes.homepage),
    ],
)