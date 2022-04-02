import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
with open('/Users/maximkalinchenko/Desktop/personal_finanse_tracker/classified.json') as secret_file:
    secrets = json.load(secret_file)
    user,passord=secrets['db']['user'],secrets['db']['password']
engine = create_engine(f'postgresql://{user}:{passord}@127.0.0.1:5432/personal_finance_tracker')
Session = sessionmaker(engine)
