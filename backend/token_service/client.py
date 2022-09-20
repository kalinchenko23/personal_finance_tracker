import plaid
import json
import pathlib
from plaid.api import plaid_api
with open (f'{pathlib.Path.cwd().parents[0]}/classified.json') as secret_file:
    secrets = json.load(secret_file)
    client_id,secret=secrets['token']['clientId'],secrets['token']['secret']

config = plaid.Configuration(host=plaid.Environment.Development,
                            api_key={'clientId': client_id,
                            'secret': secret})
api_client = plaid.ApiClient(config)
client = plaid_api.PlaidApi(api_client)

