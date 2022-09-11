from client import client
from plaid.model.country_code import CountryCode
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser


def update_token(client:client, old_access_token, client_id:str):
    request = LinkTokenCreateRequest(
        client_name="US ARMY",
        country_codes=[CountryCode('US')],
        language='en',
        access_token=old_access_token,
        user=LinkTokenCreateRequestUser(client_user_id=client_id)
    )
    resp = client.link_token_create(request)
    return resp["link_token"]
