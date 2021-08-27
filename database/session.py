from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import psycopg2
engine = create_engine('postgresql://maximkalinchenko:Maxjordan0962846325@127.0.0.1:5432/personal_finance')
Session = sessionmaker(engine)
