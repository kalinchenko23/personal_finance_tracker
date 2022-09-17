import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
with open('/home/ubuntu/personal_finance_tracker/backend/classified.json') as secret_file:
    secrets = json.load(secret_file)
    user,password=secrets['db']['user'],secrets['db']['password']
    
    endpoint_aws, user_aws, password_aws, db_name_aws, port_aws = secrets['aws']['endpoint'], secrets['aws']['user'], secrets['aws'][
        'password'], secrets['aws']['dbname'], \
                                              secrets['aws']['port']
engine = create_engine(f'postgresql://{user}:{password}@127.0.0.1:5432/personal_finance_tracker')
Session = sessionmaker(engine)

SQLALCHEMY_AWS_DATABASE_URI = f'postgresql://{user_aws}:{password_aws}@{endpoint_aws}:{port_aws}/{db_name_aws}'
engine_aws = create_engine(SQLALCHEMY_AWS_DATABASE_URI, echo=True)
Session_aws = sessionmaker(engine_aws)
