# SPDX-FileCopyrightText: 2023 peepo.world developers
#
# SPDX-License-Identifier: EUPL-1.2

from starlette.config import Config


config = Config('.env')

DEBUG = config('DEBUG', cast=bool, default=False)
WEBSITE_URL = config('WEBSITE_URL', cast=str, default='http://127.0.0.1:8000')
