import sys
import pathlib
sys.path.insert(0, f'{pathlib.Path(__file__).parents[2]}/plaid_service')
import datetime
import bcrypt
from decimal import Decimal
from typing import Optional, List
from pydantic import BaseModel,create_model, validator, Field, EmailStr
from plaid_dashboard import plaid_service

def hash_password(password: str, salt=bcrypt.gensalt()):
    hashed_pass = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_pass


class Expenses_pydantic(BaseModel):
    created_date: datetime.date = Field(alias='date')
    amount: Decimal
    account_id: str
    transaction_id: str


    class Config:
        extra = 'ignore'


class Expenses_additional_info_pydantic(BaseModel):
    transaction_id: str
    category: List
    merchant_name: str | None


    @validator('category')
    def category_check(cls, v):
        return v[-1]

    class Config:
        extra = 'ignore'


class Accounts_pydantic(BaseModel):
    id: str = Field(alias='account_id')
    name: str
    balance: Decimal = Field(alias='balances')
    subtype: str
    user_id: int

    # argument pre specifies that this validation will occur prior to
    # all other validations including field type validation
    @validator('balance', pre=True)
    def current_balance(cls, v):
        return v['current']

class Users_pydantic(BaseModel):
    username: EmailStr
    password: bytes
    first_name: str
    last_name: str

    @validator('password', pre=True)
    def hashing_p(cls, v):
        if type(v) != bytes:
            v = hash_password(v)
        return v

class Users_pydantic_out(BaseModel):
    data: Users_pydantic
    message: str

class Users_pydantic_out_wrapper(BaseModel):
    detail: Users_pydantic_out

class Tokens_pydantic(BaseModel):
    user_id: int
    bank_name: Optional[str]
    token: str
    @validator('bank_name', pre=True)
    def hashing_p(cls, v):
        inst_id=plaid_service.get_institutions_id(token)
        v=plaid_service.get_institutions_name(inst_id)
        return v
