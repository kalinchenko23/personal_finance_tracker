import sys
sys.path.insert(0, '/Users/maximkalinchenko/Desktop/personal_finance_tracker/backend/database/sql_service ')
import datetime
from sqlalchemy import select, Column, Integer, DateTime, String, ForeignKey, Float
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy_utils import database_exists, create_database

from session_sql import engine_aws, SQLALCHEMY_AWS_DATABASE_URI , Session_aws
from pydantic_models import User_pydantic
base = declarative_base()


class User(base):
    __tablename__ = "users"
    id: int = Column(Integer, primary_key=True)
    username: str = Column(String)
    password: str = Column(String)
    last_name: str = Column(String)
    first_name: str = Column(String)

def get_user(session: Session_aws,username:str):
    with Session_aws() as sess:
        stmt=select(User).where(User.username==username)
        return sess.scalars(stmt).first()


def create_user(session: Session_aws, user: User_pydantic):
    with Session_aws() as sess:
        sess.add(User(**user.dict()))

def create_tables():
    base.metadata.create_all(engine_aws)

# create_tables()
user_to_add={"username":"testuser","first_name":"Alex","last_name":"Blik"}
print(create_user(Session_aws,User_pydantic(**user_to_add)))