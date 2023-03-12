# SPDX-FileCopyrightText: 2023 peepo.world developers
#
# SPDX-License-Identifier: EUPL-1.2

import contextlib

from typing import AsyncIterator

from starlette.applications import Starlette
from starlette.routing import Route

import greenhouse.web

from greenhouse.web import db, routes


@contextlib.asynccontextmanager
async def lifespan(app: Starlette) -> AsyncIterator[None]:
    async with db.lifespan(app):
        yield



app = Starlette(
    debug=greenhouse.web.DEBUG,
    routes=[
        Route('/', routes.homepage),
    ],
    lifespan=lifespan,
)
