import mongoengine
import sshtunnel
from sshtunnel import SSHTunnelForwarder
from MongoDB_service import inserting_transactions_updating_accounts
from mongo_connection_service import connection_mongo_aws
with sshtunnel.open_tunnel(
    ('ec2-3-92-231-95.compute-1.amazonaws.com', 22),
    ssh_username='ubuntu',
    ssh_pkey='/Users/maximkalinchenko/Desktop/aws_keys/mongo_db_ec2_training.pem',
    remote_bind_address=('personalfinance.cluster-c5t9anke2d4o.us-east-1.docdb.amazonaws.com',27017),
    local_bind_address=('127.0.0.1',27017)) as tunnel:

    print(tunnel.tunnel_is_up)
    connection_mongo_aws()
    inserting_transactions_updating_accounts()



