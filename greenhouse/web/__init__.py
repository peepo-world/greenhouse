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

# Twitch client id & secret
TWITCH_CLIENT_ID = config('TWITCH_CLIENT_ID', cast=Secret, default='client_id')
TWITCH_CLIENT_SECRET = config('TWITCH_CLIENT_SECRET', cast=Secret, default='client_secret')
AUTH_REDIRECT_URI = config('AUTH_REDIRECT_URI', cast=str, default=f'{APP_URL}/auth')

# Google client id & secret
GOOGLE_CLIENT_ID = config('GOOGLE_CLIENT_ID', cast=Secret, default='client_id')
GOOGLE_CLIENT_SECRET = config('GOOGLE_CLIENT_SECRET', cast=Secret, default='client_secret')
