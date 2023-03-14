# SPDX-FileCopyrightText: 2023 peepo.world developers
#
# SPDX-License-Identifier: EUPL-1.2

import importlib.resources
from starlette.requests import Request
from starlette.templating import Jinja2Templates
from starlette.responses import Response

templates = Jinja2Templates(
    directory=importlib.resources.files('greenhouse.web.templates'),
)


async def homepage(request: Request) -> Response:
    return templates.TemplateResponse('index.html', {'request': request})

async def dashboard(request: Request) -> Response:
    return templates.TemplateResponse('dashboard.html', {'request': request})

async def top_emotes(request: Request) -> Response:
    return templates.TemplateResponse('top-emotes.html', {'request': request})
