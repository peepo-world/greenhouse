# SPDX-FileCopyrightText: 2023 peepo.world developers
#
# SPDX-License-Identifier: EUPL-1.2

import contextlib

from typing import AsyncIterator

from starlette.applications import Starlette
from starlette.routing import Route
from starlette.middleware.sessions import SessionMiddleware
import greenhouse.web
from greenhouse.web import db, routes
from starlette.config import Config
from starlette.datastructures import Secret


config = Config(".env")

DEBUG = config('DEBUG', cast=bool, default=False)
APP_HOST = config('APP_HOST', cast=str, default='127.0.0.1')
APP_PORT = config('APP_PORT', cast=str, default='8000')
APP_URL = config('APP_URL', cast=str, default=F'http://{APP_PORT}:{APP_PORT}')
DB_URL = config('DB_URL', cast=Secret)


@contextlib.asynccontextmanager
async def lifespan(app) -> AsyncIterator[None]:
    async with db.lifespan(app):
        yield



app = Starlette(
    debug=greenhouse.web.DEBUG,
    routes=[
        Route('/', routes.homepage),
        Route('/auth', routes.auth),
    ],
    lifespan=lifespan,
)
app.add_middleware(SessionMiddleware, secret_key="itsakey")
