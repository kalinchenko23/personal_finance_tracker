import datetime
import bcrypt
from decimal import Decimal
from typing import Optional, List
from pydantic import BaseModel, validator, Field, EmailStr


def hash_password(password: str, salt=bcrypt.gensalt()):
    hashed_pass = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_pass


class Expenses_pydantic(BaseModel):
    created_date: datetime.date = Field(alias='date')
    amount: Decimal
    account_id: str
    transaction_id: str

    @validator('created_date')
    def category_check(cls, v):
        return v.strftime("%m/%d/%Y")

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

    # argument pre specifies that this validation will occur prior to
    # all other validations including field type validation
    @validator('balance', pre=True)
    def current_balance(cls, v):
        return v['current']

    @validator('name')
    def name_change(cls, n):
        match n:
            case "MAKSYM KALINCHENKO -91008":
                n = "amex credit card"
            case "Customized Cash Rewards World Mastercard Card":
                n = "bofa credit card"
            case "More Rewards Amex":
                n = "navy credit card"
            case "CREDIT CARD":
                n = "chase credit card"
            case "TOTAL CHECKING":
                n = "chase checking"
            case "Active Duty Checking":
                n = "navy checking"
            case "Share Savings":
                n = "navy savings"
        return n


class Users_pydantic(BaseModel):
    username: EmailStr
    password: bytes
    first_name: str
    last_name: str

    @validator('password', pre=True)
    def hashing_p(cls, v):
        v = hash_password(v)
        return v
