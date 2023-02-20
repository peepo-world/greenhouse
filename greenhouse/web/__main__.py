# SPDX-FileCopyrightText: 2023 peepo.world developers
#
# SPDX-License-Identifier: EUPL-1.2

import uvicorn


if __name__ == '__main__':
    config = uvicorn.Config('greenhouse.web.asgi:app')
    server = uvicorn.Server(config)
    server.run()
