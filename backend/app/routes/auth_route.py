from pydantic import BaseModel
from fastapi import Depends
from fastapi.routing import APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.controllers.auth_controller import LoginAuthController
from app.deps.dependencies import get_session

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth")

SECRET_KEY = "892eab36714b3684fc632df3b2c7ef2616e23dc35b4fc760318ed2479b97bec8"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Auth


class Token(BaseModel):
    access_token: str
    token_type: str


@router.post("/", response_model=Token)
async def login(form_data=Depends(OAuth2PasswordRequestForm), session=Depends(get_session)):
    token = LoginAuthController.execute(session, form_data)
    return Token(access_token=token, token_type="bearer")
