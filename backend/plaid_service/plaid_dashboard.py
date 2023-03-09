import datetime
import sys
import pathlib
import time
sys.path.insert(1,f"{pathlib.Path(__file__).parents[1]}/token_service")
from plaid.model.accounts_get_request import AccountsGetRequest
from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid.model.institutions_get_by_id_request import InstitutionsGetByIdRequest
from plaid.model.country_code import CountryCode
from token_workflow import Token_dash

class Plaid_service(Token_dash):
    def __init__(self):
        super().__init__()

    def get_acounts_info(self,access_token):
        request = AccountsGetRequest(access_token=access_token)
        response = self.client.accounts_get(request)
        return response.to_dict()["accounts"]

    def get_institutions_id(self,access_token):
        request = AccountsGetRequest(access_token=access_token)
        response = self.client.accounts_get(request)
        return response.to_dict()["item"]["institution_id"]

    def get_institutions_name(self,institution_id):
        request = InstitutionsGetByIdRequest(institution_id=institution_id,country_codes=[CountryCode("US")])
        response = self.client.institutions_get_by_id(request)
        return response.to_dict()['institution']['name']

    def get_transactions(self,access_token:str, start_date: str, end_date: str):
        request = TransactionsGetRequest(access_token=access_token,start_date=start_date,end_date=end_date)
        response = self.client.transactions_get(request)
        # returning dict instead of PLAID API object.
        return response.to_dict()


plaid_service = Plaid_service()
