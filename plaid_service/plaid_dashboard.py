from datetime import date

from plaid.model.accounts_get_request import AccountsGetRequest
from plaid.model.transactions_get_request import TransactionsGetRequest
from token_service.token_workflow import token, amex, navy, chase


class Plaid_service():
    def __init__(self, amex=amex, navy=navy, chase=chase, client=token.client):
        self.navy = navy
        self.amex = amex
        self.chase = chase
        self.client = client

    def get_acounts_info(self, access_token: str):
        if access_token == "navy":
            request = AccountsGetRequest(access_token=self.navy)
        elif access_token == "amex":
            request = AccountsGetRequest(access_token=self.amex)
        else:
            request = AccountsGetRequest(access_token=self.chase)

        response = self.client.accounts_get(request)
        accounts = response['accounts']
        return accounts

    def get_transactions(self,access_token: str, start_date: str,end_date:str):
        if access_token == "navy":
            access_token = self.navy
        elif access_token == "amex":
            access_token = self.amex
        else:
            access_token = self.chase
        request = TransactionsGetRequest(
            access_token=access_token,
            start_date=start_date,
            end_date=end_date,
        )
        response = self.client.transactions_get(request)
        transactions = response['transactions']
        return transactions

plaid_service = Plaid_service()