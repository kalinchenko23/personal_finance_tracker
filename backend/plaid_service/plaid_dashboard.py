import datetime
import sys
import pathlib
import time
sys.path.insert(1,f"{pathlib.Path(__file__).parents[1]}/token_service")
from plaid.model.accounts_get_request import AccountsGetRequest
from plaid.model.transactions_get_request import TransactionsGetRequest
from token_workflow import token, amex, navy, chase, bofa


class Plaid_service():
    def __init__(self, amex=amex, navy=navy, bofa=bofa, chase=chase, client=token.client):
        self.navy = navy
        self.amex = amex
        self.chase = chase
        self.bofa = bofa
        self.client = client

    def get_acounts_info(self, bank: str):
        match bank:
            case "navy":
                request = AccountsGetRequest(access_token=self.navy)
            case "amex":
                request = AccountsGetRequest(access_token=self.amex)
            case "bofa":
                request = AccountsGetRequest(access_token=self.bofa)
            case "chase":
                request = AccountsGetRequest(access_token=self.chase)

        response = self.client.accounts_get(request)
        return response.to_dict()['accounts']

    def get_transactions(self, bank: str, start_date: str, end_date: str):
        match bank:
            case "navy":
                request = TransactionsGetRequest(access_token=self.navy,start_date=start_date,end_date=end_date)
            case "amex":
                request = TransactionsGetRequest(access_token=self.amex,start_date=start_date,end_date=end_date)
            case "bofa":
                request = TransactionsGetRequest(access_token=self.bofa,start_date=start_date,end_date=end_date)
            case "chase":
                request = TransactionsGetRequest(access_token=self.chase,start_date=start_date,end_date=end_date)

        response = self.client.transactions_get(request)
        # returning dict instead of PLAID API object.
        return response.to_dict()


plaid_service = Plaid_service()

