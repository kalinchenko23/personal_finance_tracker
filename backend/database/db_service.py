import datetime,sys
sys.path.insert(1,'/Users/maximkalinchenko/Desktop/personal_finance_tracker/backend/plaid_service')
from pydantic_models import Expenses_pydantic, Accounts_pydantic, Expenses_additional_info_pydantic
from plaid_dashboard import plaid_service

banks = ['amex', 'bofa', 'chase', 'navy']


def pydantic_validation_transactions(bank: str):
    return [Expenses_pydantic(**i).dict() for i in
            plaid_service.get_transactions(bank, datetime.date(2021, 1, 1), datetime.date.today())['transactions']]


def pydantic_validation_transactions_additional_info(bank: str):
    return [Expenses_additional_info_pydantic(**i).dict() for i in
            plaid_service.get_transactions(bank, datetime.date(2021, 1, 1), datetime.date.today())['transactions']]


def pydantic_validation_accounts(bank: str):
    accounts=[]
    for account in plaid_service.get_acounts_info(bank):
        accounts.append(Accounts_pydantic(**account).dict())
    return accounts

