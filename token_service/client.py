import plaid
from plaid.api import plaid_api


def create_client(client_id: str, client_secret: str):
    config = plaid.Configuration(host=plaid.Environment.Development,
                                 api_key={'clientId': client_id,
                                          'secret': client_secret})
    api_client = plaid.ApiClient(config)
    client = plaid_api.PlaidApi(api_client)
    return client
