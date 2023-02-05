# SPDX-FileCopyrightText: 2023 peepo.world developers
#
# SPDX-License-Identifier: EUPL-1.2

from starlette.applications import Starlette
from starlette.routing import Route
from starlette.config import Config

from sqlalchemy import create_engine, Column, Integer, String, LargeBinary, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from fastapi import Depends, FastAPI, HTTPException

import routes

config = Config('.env')


app = Starlette(
    debug=True,
    routes=[
        Route('/', routes.homepage),
    ],
)