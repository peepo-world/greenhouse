# SPDX-FileCopyrightText: 2023 peepo.world developers
#
# SPDX-License-Identifier: EUPL-1.2

import importlib.resources

from starlette.responses import Response
from starlette.requests import Request
from starlette.templating import Jinja2Templates


templates = Jinja2Templates(
    directory=importlib.resources.files('greenhouse.web.templates'),
)


async def homepage(request: Request) -> Response:
    return templates.TemplateResponse('index.html', {'request': request})
