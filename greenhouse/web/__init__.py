# SPDX-FileCopyrightText: 2023 peepo.world developers
#
# SPDX-License-Identifier: EUPL-1.2

from starlette.config import Config
from starlette.datastructures import Secret


config = Config('.env')

DEBUG = config('DEBUG', cast=bool, default=False)
APP_HOST = config('APP_HOST', cast=str, default='127.0.0.1')
APP_PORT = config('APP_PORT', cast=str, default='8000')
APP_URL = config('APP_URL', cast=str, default=F'http://{APP_PORT}:{APP_PORT}')
DB_URL = config('DB_URL', cast=Secret, default='postgresql://postgres:example@localhost/greenhouse')
