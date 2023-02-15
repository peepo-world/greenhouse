import os
import requests
from requests.api import request
from urllib.parse import urlencode


client_id = os.environ.get("TWITCH_CLIENT_ID")
client_secret = os.environ.get("TWITCH_CLIENT_SECRET")

# Need to change this when we have a domain
auth_redirect_URI = "http://localhost:8000/authorizecode"

# return access token if exists in OS env variable, otherwise call generate_access_token
def get_access_token(grant_type:str, code_token:str=None, access_token:str=None, refresh_token:str=None) -> str:
    if access_token:
        auth_valid = validate_access_token(access_token)
        if auth_valid:
            print("Token Valid")
            return access_token
        elif refresh_token:
            print("Token refreshed")
            return refresh_access_token()
    elif code_token:
        print("Generated new token")
        return generate_access_token(grant_type, code_token)
    
    else:
        ("user not logged in")

# Generate new access token and set OS env variable
def generate_access_token(grant_type:str, code_token:str) -> dict:

    token_url = "https://id.twitch.tv/oauth2/token"
    auth_body = {
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code_token,
        "grant_type": grant_type,
        "redirect_uri": auth_redirect_URI,
    }

    auth_response = requests.post(token_url, auth_body)

    auth_response_json = auth_response.json()
    print(auth_response_json)

    return auth_response_json

# Check if token is exists/valid
def validate_access_token(access_token):
    validate_url = "https://id.twitch.tv/oauth2/validate"
    headers = {
        "Authorization": f"OAuth {access_token}"
    }

    response = requests.get(url=validate_url, headers=headers)
    response_json = response.json()
    
    if response.ok and response_json.get('client_id') == client_id:
        return response_json
    
    return False

def refresh_access_token(refresh_token:str) -> str:
    refresh_url = "https://id.twitch.tv/oauth2/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    refresh_body = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }

    formatted_body = urlencode(refresh_body)

    response = requests.post(url=refresh_url, headers=headers, data=formatted_body)
    response_json = response.json()

    return response_json


def get_user_info(access_token:str):
    user_info_url ='https://id.twitch.tv/oauth2/userinfo'

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(user_info_url, headers=headers)
    response_json = response.json()

    return response_json
    
# Create general headers for requests to twitch
def get_auth_headers(access_token=None):
    if not access_token:
        access_token = get_access_token()

    headers = {
        "Client-ID": client_id,
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Accept": "*/*"
    }
    return headers

# Not sure what scopes are needed here
# auth_redirect_uri needs to be changed when we have a live site. 
# code
def get_auth_url(response_type:str):
    query_params = {
        "client_id": client_id,
        "redirect_uri": auth_redirect_URI,
        "response_type": response_type,
        "scope": 'user:read:email openid'
    }
    claims = "claims={\"userinfo\":{\"email\": null, \"preferred_username\": null}}"
    formatted_query_params = urlencode(query_params)
    # print(f"https://id.twitch.tv/oauth2/authorize?{formatted_query_params}&{claims}")
    return f"https://id.twitch.tv/oauth2/authorize?{formatted_query_params}&{claims}"


def send_twitch_request(endpoint:str, params:dict, body:dict = None, method:str = "GET", headers:dict = None):
    if not headers:
        headers = get_auth_headers()

    url = f"https://api.twitch.tv/helix/{endpoint}"

    try:

        request_data = {
            "method": method,
            "url": url,
            "headers": headers
        }

        if params:
            request_data["params"] = params

        if body:
            request_data["json"] = body

        response = requests.request(**request_data)
        response_json = response.json()

        return response_json
    
    except Exception as e:
        print(e)

def get_user_info(access_token: str):
    user_info_url = 'https://id.twitch.tv/oauth2/userinfo'
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.request(method="GET", url=user_info_url, headers=headers)
    response_json = response.json()
    return response_json