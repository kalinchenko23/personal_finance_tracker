from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from client import client


def exchange(client: client, public_token):
    request = ItemPublicTokenExchangeRequest(public_token=public_token)
    response = client.item_public_token_exchange(request)
    access_token = response['access_token']
    print(response)
    return access_token

