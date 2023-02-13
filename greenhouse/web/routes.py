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
    
    # username = 'climintine'
    # params = {
    #     "login": username,
    # }

    # response = auth.send_twitch_request(endpoint="users", params=params)
    # user_response = None
    # for user in response['data']:
    #     if user['login'] == username:
    #         user_response = user
    
    # user_auth url needs argument=token for implicit, code for code
    return templates.TemplateResponse('index.html', {
        'user_auth_url': auth.get_auth_url("code"), 
        'request': request})


async def authorize(request):
    return templates.TemplateResponse('authimplicit.html', {'request': request})

async def authorize_code(request):
    return templates.TemplateResponse('authcode.html', {'request': request})

async def set_variables(request):
    access_token = request.path_params['access_token']
    token_type = request.path_params['token_type']

    token = auth.get_access_token(grant_type="authorization_code", code_token=access_token)
    print(auth.get_user_info(access_token=token))

    return JSONResponse({'user_info': auth.get_user_info(access_token=access_token)})