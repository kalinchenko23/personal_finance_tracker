import sys
import pathlib
import jwt
import sqlalchemy
sys.path.insert(0, f'{pathlib.Path(__file__).parents[2]}/token_service')
sys.path.insert(1, f'{pathlib.Path(__file__).parents[2]}/database')
sys.path.insert(2, f'{pathlib.Path(__file__).parents[2]}/database/fastapi_sql')
from fastapi import FastAPI, BackgroundTasks, Query, Body, HTTPException, Depends, Body, APIRouter
from dependencies import get_session, oauth2_scheme
from token_workflow import Token_dash
from token_service import create_access_token
from user_service import get_user, create_user, authenticate_user, get_current_user
from jwt_token_service import jwt_t_service
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic_service.pydantic_models import Users_pydantic, Users_pydantic_out_wrapper
from fastapi.responses import JSONResponse
from mongoDB.fastapi_mongo.user_service import user_mongo
router = APIRouter()


@router.post("/login", responses={404:{'description':'User not found!'}})
async def login_for_access_token(username: str = Body(), password: str = Body(),
                                 session: AsyncSession = Depends(get_session)):
    user = await get_user(session, username)
    if not user:
        raise HTTPException(status_code=403, detail={"message":"Username or password does not match.","data":""})
    if not await authenticate_user(session, username, password):
        raise HTTPException(status_code=403, detail={"message":"Username or password does not match.","data":""})
    jwt_token = jwt_t_service.create_jwt_token(user)
    return {"detail":{"data":{"access_token": jwt_token, "token_type": "bearer"},"message":"JWT token was created!"}}


@router.post("/create_user/", status_code=201, response_model=Users_pydantic_out_wrapper,
             response_model_exclude={"detail":{"data":{"password"}}})

async def new_user(user: Users_pydantic, session: AsyncSession = Depends(get_session)):
    try:
        user_mongo.create_user(user)
        await create_user(session, user)
        return {"detail":{"data":user,"message":"user was created!"}}
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(status_code=400, detail={"message":"User already exist","data":""})


@router.get("/user/home")
async def read_user(session: AsyncSession = Depends(get_session), jwt_token: str = Depends(oauth2_scheme)):
    user = await get_current_user(session, jwt_token)
    return {"detail":{"data":user,"message":"current logged in user"}}

