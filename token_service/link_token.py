from plaid.model.country_code import CountryCode
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.products import Products

from .client import create_client


def create_link_token(client: create_client, client_id:str):
    request = LinkTokenCreateRequest(
        products=[Products("transactions")],
        client_name="US ARMY",
        country_codes=[CountryCode('US')],
        language='en',
        user=LinkTokenCreateRequestUser(client_user_id=client_id)
    )
    resp = client.link_token_create(request)
    return resp["link_token"]

