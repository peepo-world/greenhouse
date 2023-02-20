import requests
import json
from minio import Minio
from pathlib import Path
from urllib.parse import urlencode

db_uri = 'http://127.0.0.1:8001'

# Add user to postgres db
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

# Get user based on user id or user name.
def get_user(user_name:str = None, user_id:int = None):
    user_url = db_uri + '/users/user?'

    headers = {
        "Content-Type": "application/json",
        "Accepts": "*/*"
    }

    query_params = {}
    if user_name:
        query_params["user_name"] = user_name

    if user_id:
        query_params["user_id"] = user_id
    formatted_query_params = urlencode(query_params)

    response = requests.request(method="GET", url=user_url+formatted_query_params, headers=headers)
    response_json = response.json()
    return response_json

# Add emote to postgres db
def post_emote_postgres(owner_id:int, access:bool, name:str, object_name:str, command:str):
    user_url = db_uri + '/emotes'

    headers = {
        "Content-Type": "application/json",
        "Accepts": "*/*"
    }

    body = {
        "owner_id": owner_id,
        "access": access,
        "name": name,
        "object_name": object_name,
        "command": command
    }

    response = requests.post(user_url, data=json.dumps(body), headers=headers)

    return response

# Get emote data from postgres
def get_emotes_postgres(limit=18):
    emote_url = db_uri + '/emotes'
    headers = {
        "Content-Type": "application/json",
        "Accepts": "*/*"
    }
    
    response = requests.get(emote_url, headers=headers)
    return response.json()

# Add img object to minio db
def put_object(client: Minio, bucket_name:str, object_name:str, object: object, file_length:int):
    result = client.put_object (
        bucket_name = bucket_name, 
        object_name = object_name, 
        data = object,
        length = file_length
    )
    return result

# Get img object from minio db
def get_object(client: Minio, bucket_name:str, object_name:str):
    try:
        response = client.get_object(bucket_name=bucket_name, object_name=object_name)
    # Read data from response.
    finally:
        data = response.data
        response.close()
        response.release_conn() 
        return data
    
# Get local minio client
def get_client():
    client = Minio("127.0.0.1:9000", access_key = "minioadmin", secret_key = "minioadmin", secure = False)
    return client

# Parse file extension from uploaded img file in form
def get_file_extension(file_name:str) -> str:
    file_extension = Path(file_name).suffix
    return file_extension