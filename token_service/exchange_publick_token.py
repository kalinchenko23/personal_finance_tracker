from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from client import create_client


def exchange(client: create_client, public_token):
    request = ItemPublicTokenExchangeRequest(public_token=public_token)
    response = client.item_public_token_exchange(request)
    access_token = response['access_token']
    return access_token
