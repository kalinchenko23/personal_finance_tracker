import datetime

from database.pydantic_models import Expenses_pydantic, Accounts_pydantic, Expenses_additional_info_pydantic
from plaid_service.plaid_dashboard import plaid_service

banks = ['amex', 'bofa', 'chase', 'navy']


def pydantic_validation_transactions(bank: str):
    return [Expenses_pydantic(**i).dict() for i in
            plaid_service.get_transactions(bank, datetime.date(2021, 1, 1), datetime.date.today())['transactions']]


def pydantic_validation_transactions_additional_info(bank: str):
    return [Expenses_additional_info_pydantic(**i).dict() for i in
            plaid_service.get_transactions(bank, datetime.date(2021, 1, 1), datetime.date.today())['transactions']]


def pydantic_validation_accounts(bank: str):
    return Accounts_pydantic(**plaid_service.get_acounts_info(bank)).dict()
