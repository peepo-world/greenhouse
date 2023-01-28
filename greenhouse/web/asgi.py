# SPDX-FileCopyrightText: 2023 peepo.world developers
#
# SPDX-License-Identifier: EUPL-1.2

from starlette.applications import Starlette
from starlette.routing import Route

import greenhouse.web

from greenhouse.web import routes


app = Starlette(
    debug=greenhouse.web.DEBUG,
    routes=[
        Route('/', routes.homepage),
    ],
)
