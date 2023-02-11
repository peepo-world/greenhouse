import os
import requests
from requests.api import request
from urllib.parse import urlencode


client_id = os.environ.get("TWITCH_CLIENT_ID")
client_secret = os.environ.get("TWITCH_CLIENT_SECRET")

# Need to change this when we have a domain
auth_redirect_URI = "http://localhost:8000/authorizecode"

# return access token if exists in OS env variable, otherwise call generate_access_token
def get_access_token():
    access_token = os.environ.get("TWITCH_ACCESS_TOKEN")
    auth_valid = validate_access_token(access_token)
    if auth_valid:
        return access_token
    return generate_access_token()

# Generate new access token and set OS env variable
def generate_access_token():

    token_url = "https://id.twitch.tv/oauth2/token"
    
    auth_body = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials"
    }
    auth_response = requests.post(token_url, auth_body)

    auth_response_json = auth_response.json()

    access_token = auth_response_json['access_token']
    
    os.environ["TWITCH_ACCESS_TOKEN"] = access_token

    return access_token

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
def get_auth_url(response_type:str):
    query_params = {
        "client_id": client_id,
        "redirect_uri": auth_redirect_URI,
        "response_type": response_type,
        "scope": 'user:read:email'
    }
    formatted_query_params = urlencode(query_params)
    return f"https://id.twitch.tv/oauth2/authorize?{formatted_query_params}"


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