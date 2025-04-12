from store_app.db.database import SessionLocal
from fastapi import Depends, HTTPException, APIRouter, status
from sqlalchemy.orm import Session
from typing import List, Optional
from starlette.requests import Request
from store_app.config import (GITHUB_CLIENT_ID, GITHUB_KEY, GITHUB_URL)
from authlib.integrations.starlette_client import OAuth


oauth = OAuth()
oauth.register(
    name='github',
    client_id=GITHUB_CLIENT_ID,
    secret_key=GITHUB_KEY,
    authorize_url='http://github.com/login/oauth/authorize',
)
oauth.register(
    name='google',
    client_id= '',
    secret_key = '',
    authorize_url = 'http://accounts.google.com/o/oauth2/auth',
    client_kwargs={'scope': 'openid profile email'},
)


social_router = APIRouter(prefix='/oauth', tags=['Oauth'])

@social_router.get('/github')
async def login_github(request: Request):
    redirect_uri = GITHUB_URL
    return await oauth.github.authorize_redirect(request, redirect_uri)

