import datetime
import sys
import pathlib
import time
sys.path.insert(1,f"{pathlib.Path(__file__).parents[1]}/token_service")
from plaid.model.accounts_get_request import AccountsGetRequest
from plaid.model.transactions_get_request import TransactionsGetRequest
from token_workflow import Token_dash

class Plaid_service(Token_dash):
    def __init__(self, access_token):
        super().__init__()
        self.access_token = access_token


    def get_acounts_info(self):
        request = AccountsGetRequest(access_token=self.access_token)
        response = self.client.accounts_get(request)
        return response.to_dict()['accounts']

    def get_transactions(self, start_date: str, end_date: str):
        request = TransactionsGetRequest(access_token=self.access_token,start_date=start_date,end_date=end_date)
        response = self.client.transactions_get(request)
        # returning dict instead of PLAID API object.
        return response.to_dict()


plaid_service = Plaid_service
