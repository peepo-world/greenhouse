# SPDX-FileCopyrightText: 2023 peepo.world developers
#
# SPDX-License-Identifier: EUPL-1.2

import importlib.resources

from starlette.templating import Jinja2Templates
from starlette.responses import JSONResponse

from methods import auth


templates = Jinja2Templates(
    directory=importlib.resources.files('templates'),
)


async def homepage(request):
    return templates.TemplateResponse('index.html', {'request': request})

async def dashboard(request):
    return templates.TemplateResponse('dashboard.html', {'request': request})

async def top_emotes(request):
    return templates.TemplateResponse('top-emotes.html', {'request': request})

async def homepage(request):
    
    username = 'climintine'
    params = {
        "login": username,
    }

    response = auth.send_twitch_request(endpoint="users", params=params)
    user_response = None
    for user in response['data']:
        if user['login'] == username:
            user_response = user
    
    return templates.TemplateResponse('index.html', {
        'twitch_user': user_response,
        'user_auth_url': auth.get_auth_url("code"), 
        'request': request})


async def authorize(request):
    return templates.TemplateResponse('authimplicit.html', {'request': request})

async def authorize_code(request):
    return templates.TemplateResponse('authcode.html', {'request': request})

async def set_variables(request):
    access_token = request.path_params['access_token']
    scope = request.path_params['scope']

    return JSONResponse({'scope': scope,
                          'access_token': access_token})