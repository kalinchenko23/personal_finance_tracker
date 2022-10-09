import json
import pathlib
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
with open(f'{pathlib.Path(__file__).parents[2]}/classified.json') as secret_file:
    secrets = json.load(secret_file)
    user,password=secrets['db']['user'],secrets['db']['password']
    
    endpoint_aws, user_aws, password_aws, db_name_aws, port_aws = secrets['aws']['endpoint'], secrets['aws']['user'], secrets['aws'][
        'password'], secrets['aws']['dbname'], \
                                              secrets['aws']['port']

# localhost connection
engine = create_async_engine(f'postgresql+asyncpg://{user}:{password}@127.0.0.1:5432/personal_finance_tracker')
Session = sessionmaker(engine,expire_on_commit=False, class_=AsyncSession)

# AWS connection
SQLALCHEMY_AWS_DATABASE_URI = f'postgresql+asyncpg://{user_aws}:{password_aws}@{endpoint_aws}:{port_aws}/{db_name_aws}'
engine_aws = create_async_engine(SQLALCHEMY_AWS_DATABASE_URI, echo=True)
Session_aws = sessionmaker(engine_aws,expire_on_commit=False, class_=AsyncSession)