import json
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
    def __init__(self, old_access_token=None, public_token=None, access_token_to_remove=None,
                 client_id=client_id):
        self.old_access_token = old_access_token
        self.public_token = public_token
        self.access_token_to_remove = access_token_to_remove
        self.client=client
        self.client_id=client_id


    def create_link(self):
        link_token=create_link_token(self.client,self.client_id)
        return link_token

    def update_mode(self):
        linc_token_update_mode=update_token(self.client,self.old_access_token,self.client_id)
        return linc_token_update_mode

    def access_token(self):
        access_token=exchange(self.client,self.public_token)
        return access_token

    def remove_access_token(self):
        request=ItemRemoveRequest(access_token=self.access_token_to_remove)
        self.client.item_remove(request)
        return f"{self.access_token_to_remove} was removed"

