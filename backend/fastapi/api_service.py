import sys
import sqlalchemy
import pathlib
import uvicorn
import asyncio
import jwt
sys.path.insert(0, f'{pathlib.Path(__file__).parents[1]}/plaid_service')
sys.path.insert(1, f'{pathlib.Path(__file__).parents[1]}/database')
sys.path.insert(2, f'{pathlib.Path(__file__).parents[1]}/database/fastapi_sql')
sys.path.insert(3, f'{pathlib.Path(__file__).parents[1]}/database/sql_service')
from fastapi import FastAPI, Query, Body, HTTPException, Depends, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.cors import CORSMiddleware
from plaid_dashboard import plaid_service
from pydantic_service.pydantic_models import Users_pydantic, Tokens_pydantic
from pydantic import BaseModel
from session_sql import Session_aws
from user_service import get_user, create_user, authenticate_user, get_current_user
from jwt_token_service import create_jwt_token
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies import get_session, oauth2_scheme
from routers import plaid_token, user

app = FastAPI()
app.include_router(plaid_token.router)
app.include_router(user.router)
data = plaid_service.get_acounts_info

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_event_handler("startup",get_session)


@app.get("/")
def status_check():
    return {"message": "It's working!"}

if __name__ == "__main__":
    uvicorn.run(app)