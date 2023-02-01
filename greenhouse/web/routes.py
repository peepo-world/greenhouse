# SPDX-FileCopyrightText: 2023 peepo.world developers
#
# SPDX-License-Identifier: EUPL-1.2

import importlib.resources

from starlette.templating import Jinja2Templates


templates = Jinja2Templates(
    directory=importlib.resources.files('templates'),
)


async def homepage(request):
    return templates.TemplateResponse('index.html', {'request': request})
