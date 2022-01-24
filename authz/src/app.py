import secrets

from fastapi import FastAPI, status
from starlette.config import Config
from starlette.requests import Request
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import HTMLResponse, RedirectResponse
from authlib.integrations.starlette_client import OAuth, OAuthError
from fastapi.responses import JSONResponse

from helper import create_json_user, user_exists
from config import email_scope

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=secrets.token_urlsafe(32))

config = Config('.env')
oauth = OAuth(config)

CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth.register(
    name='google',
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)

@app.get('/')
async def home(request: Request):
    user = request.session.get('user')
    redi = request.session.get('caller')
    if redi is None:
        if user is not None:
            if user["email"].split("@")[1] != email_scope:
                return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED)
            result = user_exists(user)
            if result is False:
                created_user = create_json_user(user)
                if not created_user:
                    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND)
            return JSONResponse(status_code=status.HTTP_200_OK, content=user)
        return HTMLResponse('<a href="/login">login</a>')
    request.session.pop('caller', None)
    return RedirectResponse(url='/'+ redi)

@app.get('/login', tags=['authentication'])  # Tag it as "authentication" for our docs
async def login(request: Request):
    redirect_uri = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@app.route('/auth')
async def auth(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user = await oauth.google.parse_id_token(request, token)
    request.session['user'] = dict(user)
    return RedirectResponse(url='/')

@app.get('/logout', tags=['authentication'])  # Tag it as "authentication" for our docs
async def logout(request: Request):
    request.session.pop('user', None)
    request.session.pop('caller', None)
    return RedirectResponse(url='/')

@app.get('/permissions', tags=['authorization']) # Tag it as "authorization" for our docs
async def permissions(request: Request):
    user = request.session.get('user')
    if user is not None:
        return HTMLResponse('permissions_end_point')
    else:
        request.session['caller'] = 'permissions'
        return RedirectResponse(url='/login')

@app.get('/authorize', tags=['authorization']) # Tag it as "authorization" for our docs
async def authorize(request: Request):
    user = request.session.get('user')
    if user is not None:
        return HTMLResponse('authorize_end_point')
    else:
        request.session['caller'] = 'authorize'
        return RedirectResponse(url='/login')

@app.get('/token', tags=['authorization']) # Tag it as "authorization" for our docs
async def token(request: Request):
    user = request.session.get('user')
    if user is not None:
        return HTMLResponse('token_end_point')
    else:
        request.session['caller'] = 'token'
        return RedirectResponse(url='/login')