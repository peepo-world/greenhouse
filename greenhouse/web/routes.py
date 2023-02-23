# SPDX-FileCopyrightText: 2023 peepo.world developers
#
# SPDX-License-Identifier: EUPL-1.2

import importlib.resources

from starlette.templating import Jinja2Templates
from starlette.requests import Request
from starlette.responses import JSONResponse, RedirectResponse
import os
from requests_oauthlib import OAuth2Session
import time

import greenhouse.web


twitch_client_id = greenhouse.web.TWITCH_CLIENT_ID
twitch_client_secret = greenhouse.web.TWITCH_CLIENT_SECRET

google_client_id = greenhouse.web.GOOGLE_CLIENT_ID
google_client_secret = greenhouse.web.GOOGLE_CLIENT_SECRET

auth_redirect_URI = greenhouse.web.AUTH_REDIRECT_URI
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' # Remove for production - makes it so you can use http for redirect
############################################################################
####                Twitch specific endpoints, params                   ####
twitch_auth_base_url = "https://id.twitch.tv/oauth2/authorize"
twitch_token_url = "https://id.twitch.tv/oauth2/token"
twitch_token_refresh_url = twitch_token_url
twitch_userinfo_url = "https://id.twitch.tv/oauth2/userinfo"
scope = ['user:read:email openid']
claims = "claims={\"userinfo\":{\"email\": null, \"preferred_username\": null}}"

############################################################################
####                Google specific endpoints, params                   ####
google_auth_base_url = "https://accounts.google.com/o/oauth2/v2/auth"
google_token_url = "https://oauth2.googleapis.com/token"
google_token_refresh_url = google_token_url
google_userinfo_url = "https://openidconnect.googleapis.com/v1/userinfo"
google_scope = [
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "openid"
]
############################################################################

templates = Jinja2Templates(
    directory=importlib.resources.files('greenhouse.web.templates'),
)

async def homepage(request:Request):
    return templates.TemplateResponse('index.html', {'request': request})

# Template so user can select preferred oauth provider
async def login(request:Request):
    return templates.TemplateResponse('login.html', {'request': request})

# Create auth url for oauth provider selected in /login
async def generate_auth_url(request:Request):
    authenticator = request.path_params['authenticator']
    request.session['authenticator'] = authenticator

    if authenticator == 'twitch':
        oauth_session = OAuth2Session(twitch_client_id, redirect_uri=auth_redirect_URI, scope=scope)
        authorization_url, state = oauth_session.authorization_url(twitch_auth_base_url, claims=claims)
        request.session['state'] = state
        
    if authenticator == 'youtube':
        oauth_session = OAuth2Session(google_client_id, redirect_uri=auth_redirect_URI, scope=google_scope)
        authorization_url, state = oauth_session.authorization_url(google_auth_base_url, access_type='offline')
        request.session['state'] = state
    
    return RedirectResponse(authorization_url)

# Get acces token via OIDC. JSON response of token dictionary
async def auth(request:Request):
    # Fetch token from Twitch
    if request.session['authenticator'] == 'twitch':
        oauth_session = OAuth2Session(twitch_client_id, redirect_uri=auth_redirect_URI, state=request.session['state'])
        authorization_response = str(request.url)
        token_dict = oauth_session.fetch_token(twitch_token_url, client_secret=twitch_client_secret,
                                    authorization_response=authorization_response,
                                    include_client_id=True)
        
        # Get User info -> dict
        user_info = oauth_session.get(url=twitch_userinfo_url)
        user_info_json = user_info.json()

        # username is not a field in googles userinfo 
        request.session['username'] = user_info_json['preferred_username']

    # Fetch token from Google
    if request.session['authenticator'] == 'youtube':
        oauth_session = OAuth2Session(google_client_id, redirect_uri=auth_redirect_URI, state=request.session['state'])
        authorization_response = str(request.url)
        token_dict = oauth_session.fetch_token(google_token_url, client_secret=google_client_secret,
                                    authorization_response=authorization_response,
                                    include_client_id=True)
        # Get user info -> dict
        user_info = oauth_session.get(url=google_userinfo_url)
        user_info_json = user_info.json()

    # Add user/auth info to session
    request.session['access_token'] = token_dict['access_token']
    request.session['refresh_token'] = token_dict['refresh_token']
    request.session['expires_at'] = token_dict['expires_at']
    request.session['user_id'] = user_info_json['sub']
    

    # Return JSON of fetched token. Probably want to return RedirectResponse moving forward
    return JSONResponse({"token":token_dict, "user_info": user_info_json})
 
# Pass expired token back to oauth client to refresh
# For some reason this seems to refresh whether expires_in is negative or not.
async def refresh_token(request:Request):
    token = {
        'access_token': request.session['access_token'],
        'refresh_token': request.session['refresh_token'],
        'token_type': 'Bearer',
        'expires_in': request.session['expires_at'] - time.time(),
    }
    if request.session['authenticator'] == 'twitch':
        oauth_session = OAuth2Session(twitch_client_id, 
                                      token=token,
                                      redirect_uri=auth_redirect_URI)
        token_dict = oauth_session.refresh_token(twitch_token_refresh_url, 
                                    client_id=twitch_client_id,
                                    client_secret=twitch_client_secret)
        
    if request.session['authenticator'] == 'youtube':
        oauth_session = OAuth2Session(google_client_id, 
                                      token=token,
                                      redirect_uri=auth_redirect_URI)
        token_dict = oauth_session.refresh_token(google_token_refresh_url, 
                                    client_id=google_client_id,
                                    client_secret=google_client_secret)
        
    request.session['access_token'] = token_dict['access_token']
    request.session['refresh_token'] = token_dict['refresh_token']
    request.session['expires_at'] = token_dict['expires_at']

    return JSONResponse(token_dict)

