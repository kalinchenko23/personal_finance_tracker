import json
import plaid
from pathlib import Path
from client import client
from link_token import create_link_token
from exchange_publick_token import exchange
from update_mode import update_token
from plaid.model.item_remove_request import ItemRemoveRequest

with open(Path(__file__).parents[1] / 'classified.json', 'r') as f:
    secrets = json.load(f)
    chase, amex, navy, bofa =[v for v in secrets['credentials'].values()]
    client_id = secrets["token"]["clientId"]

class Token_dash():
    def __init__(self,
                 client_id=client_id):
        self.client=client
        self.client_id=client_id


    def create_link(self):
        link_token=create_link_token(self.client,self.client_id)
        return link_token

    def update_mode(self,access_token):
        linc_token_update_mode=update_token(self.client,access_token,self.client_id)
        return linc_token_update_mode

    def access_token(self,public_token):
        access_token=exchange(self.client, public_token)
        return access_token

    def remove_access_token(self,access_token):
        request=ItemRemoveRequest(access_token=access_token)
        self.client.item_remove(request)
        return f"{access_token} was removed"
