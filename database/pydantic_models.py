import datetime
from decimal import Decimal
from typing import Optional, List

from pydantic import BaseModel, validator, Field


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
