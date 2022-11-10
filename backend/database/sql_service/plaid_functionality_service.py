import sys
import asyncio
import pathlib
import datetime

sys.path.insert(1, f'{pathlib.Path(__file__).parents[1]}')
from sqlalchemy import select, update
from session_sql import Session_aws
from pydantic_service.pydantic_validation import transactions, transactions_additional_info, accounts
from db_tables import Expenses, Expenses_additional_info, Accounts


# This class is responsible for writing and updating entities to SQL DB
class DB_service():
    def __init__(self, session, access_token):
        self.session = session
        self.access_token = access_token

    async def insertORupdate_account_info(self, user_id):
        for account in accounts(self.access_token, user_id):
            res = await self.session.execute(select(Accounts).filter(Accounts.id == account.id))
            if res.scalars().first() is None:
                print("inserting")
                self.session.add(Accounts(**account.dict()))
            else:
                print("updating")
                stmt = (
                    update(Accounts).
                        where(Accounts.id == account.id).
                        values(**account.dict())
                )
                await self.session.execute(stmt)

    async def insert_transactions(self, start_date: datetime.datetime, stop_date: datetime.datetime):
        async with self.session() as sess, sess.begin():
            for row in transactions(self.access_token, start_date, stop_date):
                res= await sess.execute(select(Expenses).filter(Expenses.transaction_id == row.transaction_id))
                if res.scalars().first() is None:
                    sess.add(Expenses(**row.dict()))
            for row in transactions_additional_info(self.access_token, start_date, stop_date):
                res= await sess.execute(select(Expenses_additional_info).filter(Expenses_additional_info.transaction_id == row.transaction_id))
                if res.scalars().first() is None:
                    sess.add(Expenses_additional_info(**row.dict()))



# service = DB_service(Session_aws, "access-development-34d02990-da5b-4c13-9ae7-7293ced2bb42")
#
# async def main():
#     await service.insert_transactions(datetime.date(2022, 1, 5), datetime.date.today())
# asyncio.run(main())
