from store_app.db.models import UserProfile, RefreshToken, Cart
from store_app.db.schema import UserProfileSchema, UserLoginSchema
from store_app.db.database import SessionLocal
from fastapi import Depends, HTTPException, APIRouter, status
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from typing import Optional, List
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import jwt
from store_app.config import (SECRET_KEY, ALGORITHM,
                              ACCESS_TOKEN_EXPIRE_MINUTES,
                              REFRESH_TOKEN_EXPIRE_DAYS)


oauth2_schema = OAuth2PasswordBearer(tokenUrl='/auth/login/')
password_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict):
    return create_access_token(data, expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))

def verify_password(plan_password, password):
    return password_context.verify(plan_password, password)

def get_password_hash(password):
    return password_context.hash(password)


auth_router = APIRouter(prefix='/auth', tags=['Authorization'])


@auth_router.post('/register', response_model=dict)
async def auth_create(user: UserProfileSchema, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.username == user.username).first()
    email_db = db.query(UserProfile).filter(UserProfile.email == user.email).first()
    if user_db:
        raise HTTPException(status_code=401, detail='This username is already exist')
    elif email_db:
        raise HTTPException(status_code=401, detail='This email is already exist')

    new_password = get_password_hash(user.password)
    new_user = UserProfile(
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        email=user.email,
        age=user.age,
        phone_number=user.phone_number,
        status=user.status,
        created_date=user.created_date,
        password=new_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    new_cart = Cart(user_id=new_user.id)
    db.add(new_cart)
    db.commit()

    return {'message': 'Registration was successful'}



@auth_router.post('/login')
async def login(form_data: UserLoginSchema = Depends(), db: Session = Depends(get_db)):
    user = db.query(UserProfile).filter(UserProfile.email == form_data.email).first()

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=404, detail='Information is not correct')

    access_token = create_access_token({'sub': user.username})
    refresh_token = create_refresh_token({'sub': user.username})
    token_db = RefreshToken(token=refresh_token, user_id=user.id)
    db.add(token_db)
    db.commit()

    return {'access_token': access_token, 'refresh_token': refresh_token, 'token_type':'bearer'}


@auth_router.post('/logout')
async def logout(refresh_token: str, db: Session = Depends(get_db)):

    stored_token = db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()

    if not stored_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Information is not correct')

    db.delete(stored_token)
    db.commit()
    return {'message': 'Exit'}


@auth_router.post('/refresh')
def refresh(refresh_token: str, db: Session = Depends(get_db)):
    token_entry = db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()
    if not token_entry:
        raise HTTPException(status_code=401, detail='Information is not correct')

    access_token = create_access_token({'sub': token_entry.user_id})

    return {'access_token': access_token, 'token_type': 'bearer'}





























