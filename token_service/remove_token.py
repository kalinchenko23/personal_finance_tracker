from plaid.model.item_remove_request import ItemRemoveRequest

from .client import create_client


# def remove_token(client: create_client, access_token: str):
#     request = ItemRemoveRequest(access_token=access_token)
#     resp = client.item_remove(request)

def remove_token(func):
    def wrapper(*args):
        client, access_token = args
        request = ItemRemoveRequest(access_token=access_token)
        resp = client.item_remove(request)
    return func
