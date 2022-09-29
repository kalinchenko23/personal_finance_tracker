import sys
import sqlalchemy
import pathlib
import uvicorn
import asyncio
sys.path.insert(0, f'{pathlib.Path(__file__).parents[1]}/plaid_service')
sys.path.insert(1, f'{pathlib.Path(__file__).parents[1]}/database')
sys.path.insert(2, f'{pathlib.Path(__file__).parents[1]}/database/fastapi_sql')
sys.path.insert(3, f'{pathlib.Path(__file__).parents[1]}/database/sql_service')
from fastapi import FastAPI, Query, HTTPException, Depends, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.cors import CORSMiddleware
from plaid_dashboard import plaid_service
from pydantic_models import Users_pydantic
from pydantic import BaseModel
from session_sql import Session_aws
from user_service import get_user, create_user, authenticate_user, get_current_user
from fastapi.security import OAuth2PasswordBearer
from jwt_token_service import create_jwt_token
from sqlalchemy.ext.asyncio import AsyncSession
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
data = plaid_service.get_acounts_info
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def get_session():
    async with Session_aws() as sess:
        yield sess


@app.get("/")
def status_check():
    return {"message": "It's working!"}

@app.post("/login")
async def login_for_access_token(username:str, password:str, session: AsyncSession = Depends(get_session)):
    user= await get_user(session, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    if not authenticate_user(session,username,password):
        raise HTTPException(status_code=403, detail="Username or password does not match.")
    jwt_token=create_jwt_token(user)
    return {"access_token": jwt_token, "token_type": "bearer"}

@app.post("/create_user/", status_code=201)
async def new_user(user: Users_pydantic, session: AsyncSession = Depends(get_session)):
    try:
        await create_user(session, user)
        return user
    except sqlalchemy.exc.IntegrityError:
         raise HTTPException(status_code=400, detail="User already exist")


@app.get("/user/home")
async def read_user(session: AsyncSession = Depends(get_session),token: str = Depends(oauth2_scheme)):
    user =  await get_current_user(session,token)
    return user

uvicorn.run(app)
