import sys
sys.path.insert(0,'/Users/maximkalinchenko/Desktop/personal_finance_tracker/backend/database')
sys.path.insert(0,'/Users/maximkalinchenko/Desktop/personal_finance_tracker/backend/database/sql_service')
import sqlalchemy
from sqlalchemy import select
from pydantic_models import User
from session_sql import Session_aws, engine_aws
from db_tables import Users, base


def get_user(session: sqlalchemy.orm.session, username: str):
    stmt=select(Users).where(Users.username==username)
    result=session.scalars(stmt).first()
    return result

def create_user(session: sqlalchemy.orm.session, user: User):
   session.add(Users(**user.dict()))
   session.commit()

