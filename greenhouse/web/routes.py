# SPDX-FileCopyrightText: 2023 peepo.world developers
#
# SPDX-License-Identifier: EUPL-1.2

import importlib.resources

from starlette.templating import Jinja2Templates
from starlette.responses import JSONResponse, RedirectResponse
from starlette.requests import Request

from methods import auth, db

# Context processor for session stuff
def app_context(request):
    if request.session:
        return {
            'access_token': request.session['token'],
            'user_name': request.session['user_name'],
            'email': request.session['email'],
            'session':request.session, # This is mostly here for testing. probably needs to go
            'user_auth_url': auth.get_auth_url('code')
        }
    else:
        return {
            'access_token': None,
            'user_name': None,
            'email': None,
            'session': None,
            'user_auth_url': auth.get_auth_url('code')
        }
    
templates = Jinja2Templates(
    directory=importlib.resources.files('templates'),
    context_processors=[app_context],
)

async def dashboard(request):
    return templates.TemplateResponse('dashboard.html', {'request': request})

async def top_emotes(request):
    return templates.TemplateResponse('top-emotes.html', {'request': request})

async def homepage(request):
    # user_auth url needs argument=token for implicit, code for code
    return templates.TemplateResponse('index.html', {'request': request})

async def authorize(request):
    return templates.TemplateResponse('authimplicit.html', {'request': request})

async def authorize_code(request):
    return templates.TemplateResponse('authcode.html', {'request': request})

async def set_variables(request):
    # save code token str and type to variables
    code_token = request.path_params['access_token']
    token_type = request.path_params['token_type']

    # Get access token & user info (email and username)
    access_token = auth.get_access_token(grant_type="authorization_code", code_token=code_token)
    user_info = auth.get_user_info(access_token=access_token)

    # Add token properties to session
    request.session["token"] = access_token
    request.session["user_name"] = user_info['preferred_username']
    request.session["email"] = user_info['email']

    # Add user to db if it doesn't already exist
    response = db.post_user(user_info['email'], user_info['preferred_username'], user_info['sub'])
    return JSONResponse({'user_info': auth.get_user_info(access_token=code_token)})

async def get_variables(request):
    return JSONResponse({'access_token': request.session['token'],
                         'user_name': request.session['user_name'],
                         'email': request.session['email'],
                         "session":request.session})

async def clear_session(request):
    request.session.clear()
    return RedirectResponse("/")