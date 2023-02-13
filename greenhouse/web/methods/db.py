import requests
import json

db_uri = 'http://127.0.0.1:8001'

def post_user(email:str, username:str, twitch_id: str):
    user_url = db_uri + '/users'

    headers = {
        "Content-Type": "application/json",
        "Accepts": "*/*"
    }

    body = {
        "email": email,
        "user_name": username,
        "twitch_id": twitch_id
    }

    response = requests.post(user_url, data=json.dumps(body), headers=headers)

    return response