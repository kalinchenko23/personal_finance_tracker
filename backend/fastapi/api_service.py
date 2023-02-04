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
import sentry_sdk
from fastapi import FastAPI, Query, Body, HTTPException, Depends, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.cors import CORSMiddleware
from plaid_dashboard import plaid_service
from pydantic_service.pydantic_models import Users_pydantic, Tokens_pydantic
from pydantic import BaseModel
from session_sql import Session_aws
from user_service import get_user, create_user, authenticate_user, get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies import get_session, oauth2_scheme
from routers import plaid_token, user, user_data
from jwt_token_service import jwt_t_service
from user_service import get_current_user
sentry_sdk.init(dsn="https://820d3647275849e19803f04aab475e9e@o995707.ingest.sentry.io/4504001351974912",
                traces_sample_rate=1.0)
app = FastAPI()
app.include_router(plaid_token.router)
app.include_router(user.router)
app.include_router(user_data.router)
data = plaid_service.get_acounts_info

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_event_handler("startup",get_session)

@app.get("/")
def status_check():
    return {"message": f"It's working!"}

@app.get("/api/refresh")
async def refresh_jwt_access_token(session:AsyncSession = Depends(get_session), refresh_token:str = Depends(oauth2_scheme)):
    user=await get_current_user(session, refresh_token)
    if user:
        print(user)
        jwt_token=jwt_t_service.create_jwt_token(user)
        new_refresh_token=jwt_t_service.create_jwt_refresh_token(user)
        return {"message":"new jwt access token","data":{"jwt_token":jwt_token, "refresh_token":new_refresh_token}}
    else:
        {"message": "please try different refresh token", "data": refresh_token}

if __name__ == "__main__":
    uvicorn.run(app)