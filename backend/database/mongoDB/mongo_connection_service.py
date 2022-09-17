import mongoengine
import json
with open('/home/ubuntu/personal_finance_tracker/backend/classified.json') as secret_file:
    secrets = json.load(secret_file)
    user, password = secrets['db']['user'], secrets['aws']['password']

def connection_mongo():
    return mongoengine.connect('personal_finance_tracker')


def connection_mongo_aws():
    return mongoengine.connect(host=f'mongodb://{user}:{password}@localhost:27017/personal_finance_tracker?replicaSet=rs0&tls=true'
             '&tlsCAFile=/Users/maximkalinchenko/Desktop/aws_keys/rds-combined-ca-bundle.pem&tlsAllowInvalidHostnames=true'
             '&readPreference=secondaryPreferred&retryWrites=false&directConnection=true')

