# SPDX-FileCopyrightText: 2023 peepo.world developers
#
# SPDX-License-Identifier: EUPL-1.2

import importlib.resources

from starlette.templating import Jinja2Templates
from starlette.responses import JSONResponse, RedirectResponse
from starlette.requests import Request

from io import BytesIO

from os import SEEK_END
from PIL import Image
import base64

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
    emote_dict_list = db.get_emotes_postgres()
    # iterate response and get each image file, author from minio
    for emote in emote_dict_list:

        # Get object from minio and add to dict
        name = emote['name']
        object = db.get_object(client=db.get_client(), bucket_name="emotes", object_name=name)
        image_bytes = BytesIO(object)
        image = Image.open(image_bytes)
        image_rs = image.resize(size=(56,56))
        image_bytes_rs = BytesIO()
        image_rs.save(image_bytes_rs, format="png")
        data_src = 'data:image/png;base64,' + base64.b64encode(image_bytes_rs.getvalue()).decode('ascii')
        emote['object'] = data_src

        # Get owner's username
        owner = db.get_user(user_id=emote["owner_id"])
        emote['owner_name'] = owner["user_name"]
    return templates.TemplateResponse('top-emotes.html', {'request': request, 'response': emote_dict_list})

async def homepage(request):
    # user_auth url needs argument=token for implicit, code for code
    return templates.TemplateResponse('index.html', {'request': request})

# Not used currently. endpoint for implicity auth
async def authorize(request):
    return templates.TemplateResponse('authimplicit.html', {'request': request})

async def authorize_code(request):
    return templates.TemplateResponse('authcode.html', {'request': request})

async def set_variables(request):
    # save code token str and type to variables
    code_token = request.path_params['access_token']
    token_type = request.path_params['token_type']

    # Get access token & user info (email and username)
    access_token_dict = auth.get_access_token(grant_type="authorization_code", code_token=code_token)
    
    # Parse access token 
    access_token = access_token_dict["access_token"]
    refresh_token = access_token_dict["refresh_token"]
    expires_in = access_token_dict["expires_in"]

    # Request claims
    user_info = auth.get_user_info(access_token=access_token)

    # Add token properties to session
    request.session["token"] = access_token
    request.session["refresh_token"] = refresh_token
    request.session["expires_in"] = expires_in

    # Add claims properties to session
    request.session["user_name"] = user_info['preferred_username']
    request.session["email"] = user_info['email']

    # Add user to db if it doesn't already exist
    response = db.post_user(user_info['email'], user_info['preferred_username'], user_info['sub'])
    return JSONResponse({'user_info': auth.get_user_info(access_token=code_token)})

async def get_variables(request):
    auth.get_access_token(grant_type="authorization_code", access_token=request.session["token"], refresh_token=request.session["refresh_token"])
    return JSONResponse({"session":request.session})

async def clear_session(request):
    request.session.clear()
    return RedirectResponse("/")

async def upload(request):
    context = {
        'request':request
        }
    try:
        # Get data from form and save to vars
        form = await request.form()
        file_name = form["file"].filename
        file_contents = await form["file"].read()
        file_stream = BytesIO(file_contents)
        emote_name = form["emotename"] + db.get_file_extension(file_name)
        command = form["command"]

        # Get user id from db
        response = db.get_user(user_name=request.session["user_name"])
        user_id = response["id"]

        # Post data to postgres db
        response = db.post_emote_postgres(
            owner_id=user_id, 
            access=True, 
            name=emote_name, 
            object_name=emote_name,
            command=command
        )
        
        # Post image file to object store 
        if response.ok:
            result = db.put_object(client=db.get_client(), 
            bucket_name="emotes", 
            object_name=emote_name,
            object=file_stream,
            file_length=file_stream.getbuffer().nbytes
            )
            print(result)

    except Exception as e:
        print(e)
    
    return templates.TemplateResponse("upload.html", context)