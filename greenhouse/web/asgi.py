# SPDX-FileCopyrightText: 2023 peepo.world developers
#
# SPDX-License-Identifier: EUPL-1.2

from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.config import Config
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

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
        Route('/dashboard', routes.dashboard),
        Route('/top-emotes', routes.top_emotes),
        Route('/authorize', routes.authorize), # dont really need anymore
        Route('/authorizecode', routes.authorize_code),
        Route('/setvariables/{access_token}/{token_type}', routes.set_variables),
        Route('/getvariables', routes.get_variables), #For testing
        Route('/clearsession', routes.clear_session),
        Route('/upload', routes.upload, methods=["GET", "POST"]),
        Mount('/static', StaticFiles(directory='static'), name='static')
    ],
)
app.add_middleware(SessionMiddleware, secret_key="itsakey")