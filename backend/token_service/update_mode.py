from client import client
from plaid.model.country_code import CountryCode
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.link_token_create_request_update import LinkTokenCreateRequestUpdate


def update_token(client: client, old_access_token, client_id: str):
    request = LinkTokenCreateRequest(
        client_name="US ARMY",
        country_codes=[CountryCode('US')],
        language='en',
        redirect_uri="https://pf-client-kdih.vercel.app/oauth",
        access_token=old_access_token,
        user=LinkTokenCreateRequestUser(client_user_id=client_id),
        update=LinkTokenCreateRequestUpdate(account_selection_enabled=True)
        #link_customization_name="account_selection_v2_customization"
    )
    resp = client.link_token_create(request)
    return resp["link_token"]

