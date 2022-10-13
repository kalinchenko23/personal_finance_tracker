import sys
import pathlib
import jwt
import sqlalchemy
sys.path.insert(0, f'{pathlib.Path(__file__).parents[2]}/token_service')
sys.path.insert(1, f'{pathlib.Path(__file__).parents[2]}/database')
sys.path.insert(2, f'{pathlib.Path(__file__).parents[2]}/database/fastapi_sql')
from fastapi import FastAPI, Query, Body, HTTPException, Depends, Body, APIRouter
from dependencies import get_session, oauth2_scheme
from token_workflow import Token_dash
from token_service import create_access_token
from user_service import get_user, create_user, authenticate_user, get_current_user
from jwt_token_service import decode_jwt_token, create_jwt_token
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic_service.pydantic_models import Users_pydantic
router = APIRouter()


@router.post("/login")
async def login_for_access_token(username: str = Body(), password: str = Body(),
                                 session: AsyncSession = Depends(get_session)):
    user = await get_user(session, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    if not await authenticate_user(session, username, password):
        raise HTTPException(status_code=403, detail="Username or password does not match.")
    jwt_token = create_jwt_token(user)
    return {"access_token": jwt_token, "token_type": "bearer"}


@router.post("/create_user/", status_code=201)
async def new_user(user: Users_pydantic, session: AsyncSession = Depends(get_session)):
    try:
        await create_user(session, user)
        return user
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(status_code=400, detail="User already exist")


@router.get("/user/home")
async def read_user(session: AsyncSession = Depends(get_session), jwt_token: str = Depends(oauth2_scheme)):
    user = await get_current_user(session, jwt_token)
    return user
