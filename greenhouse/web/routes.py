# SPDX-FileCopyrightText: 2023 peepo.world developers
#
# SPDX-License-Identifier: EUPL-1.2

import importlib.resources

from starlette.templating import Jinja2Templates
from starlette.requests import Request
from starlette.responses import JSONResponse, RedirectResponse
import os
from requests_oauthlib import OAuth2Session

import greenhouse.web


client_id = greenhouse.web.CLIENT_ID
client_secret = greenhouse.web.CLIENT_SECRET
auth_redirect_URI = greenhouse.web.AUTH_REDIRECT_URI
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

####                Twitch specific endpoints, params                   ####
authorization_base_url = "https://id.twitch.tv/oauth2/authorize"
token_url = "https://id.twitch.tv/oauth2/token"
userinfo_url = "https://id.twitch.tv/oauth2/userinfo"
scope = ['user:read:email openid']
claims = "claims={\"userinfo\":{\"email\": null, \"preferred_username\": null}}"
############################################################################

templates = Jinja2Templates(
    directory=importlib.resources.files('greenhouse.web.templates'),
)

async def homepage(request:Request):
    oauth_session = OAuth2Session(client_id, redirect_uri=auth_redirect_URI, scope=scope)
    authorization_url, state = oauth_session.authorization_url(authorization_base_url, claims=claims)
    request.session['state'] = state
    return templates.TemplateResponse('index.html', {'request': request, 'authorization_url': authorization_url})

# Get acces token via OIDC. JSON response of token dictionary
async def auth(request:Request):
    # Fetch token from Twitch
    oauth_session = OAuth2Session(client_id, redirect_uri=auth_redirect_URI, state=request.session['state'])
    authorization_response = str(request.url)
    token_dict = oauth_session.fetch_token(token_url, client_secret=client_secret,
                                authorization_response=authorization_response,
                                include_client_id=True)
    
    # Get User info
    user_info = oauth_session.get(url=userinfo_url)
    user_info_json = user_info.json()

    # Add user/auth info to session
    request.session['access_token'] = token_dict['access_token']
    request.session['refresh_token'] = token_dict['refresh_token']

    request.session['username'] = user_info_json['preferred_username']
    request.session['user_id'] = user_info_json['sub']

    # Return JSON of fetched token. Probably want to return RedirectResponse moving forward
    return JSONResponse({"token":token_dict, "user_info": user_info_json})
 