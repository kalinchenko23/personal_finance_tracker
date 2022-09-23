import sys
import sqlalchemy
import pathlib
sys.path.insert(0, f'{pathlib.Path(__file__).parents[1]}/plaid_service')
sys.path.insert(1, f'{pathlib.Path(__file__).parents[1]}/database')
sys.path.insert(2, f'{pathlib.Path(__file__).parents[1]}/database/fastapi_sql')
sys.path.insert(3, f'{pathlib.Path(__file__).parents[1]}/database/sql_service')
from fastapi import FastAPI, Query, HTTPException, Depends, Body
import uvicorn
from plaid_dashboard import plaid_service
from pydantic_models import User
from pydantic import BaseModel
from session_sql import Session_aws
from fastapi_sql_service import get_user, create_user

data = plaid_service.get_acounts_info
app = FastAPI()


def get_session():
    sess = Session_aws()
    try:
        yield sess
    finally:
        sess.close()


@app.get("/")
def status_check():
    return {"message": "It's working!"}


@app.post("/users/", status_code=201)
def new_user(user: User, session: sqlalchemy.orm.session = Depends(get_session)):
    if get_user(session, user.dict()['username']):
        raise HTTPException(status_code=400, detail="User already exist")
    else:
        create_user(session, user)


uvicorn.run(app)
