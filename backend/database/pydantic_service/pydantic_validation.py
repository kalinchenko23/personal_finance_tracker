import datetime, sys, pathlib

sys.path.insert(1, f'{pathlib.Path(__file__).parents[2]}/plaid_service')
from .pydantic_models import Expenses_pydantic, Accounts_pydantic, Expenses_additional_info_pydantic
from plaid_dashboard import plaid_service




def transactions(access_token:str,start_date: datetime.datetime,stop_date: datetime.datetime):
    return [Expenses_pydantic(**i) for i in
            plaid_service.get_transactions(access_token, start_date, stop_date)['transactions']]


def transactions_additional_info(access_token:str,start_date: datetime.datetime,stop_date: datetime.datetime):
    return [Expenses_additional_info_pydantic(**i) for i in
            plaid_service.get_transactions(access_token, start_date, stop_date)['transactions']]


def accounts(access_token:str,user_id,bank_name,bank_id):
    accounts = []
    for account in plaid_service.get_acounts_info(access_token):
        account["user_id"]=user_id
        account["bank_name"] = bank_name
        account["bank_id"] = bank_id
        accounts.append(Accounts_pydantic(**account))
    return accounts

