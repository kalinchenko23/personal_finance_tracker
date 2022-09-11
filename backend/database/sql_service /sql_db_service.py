import sys

sys.path.insert(1, '/Users/maximkalinchenko/Desktop/personal_finance_tracker/database')
from sqlalchemy import select, update
from session_sql import Session
from db_service import pydantic_validation_transactions, pydantic_validation_transactions_additional_info, \
    pydantic_validation_accounts, banks
from db_tables import Expenses, Expenses_additional_info, Accounts


# This class is responsible for writing and updating entities to SQL DB
class DB_service():
    def __init__(self, banks, session):
        self.banks = banks
        self.session = session

    def insert_account_info(self):
        with self.session() as sess, sess.begin():
            sess.add_all([Accounts(pydantic_validation_accounts(bank)) for bank in banks if sess.execute(
                select(Accounts).filter(
                    Accounts.id == pydantic_validation_accounts(bank)['id'])).scalars().first() is None])

    def update_account_info(self):
        with self.session() as sess, sess.begin():
            for bank in self.banks:
                accounts = pydantic_validation_accounts(bank)
                for account in accounts:
                    stmt = (
                        update(Accounts).
                            where(Accounts.id == account['id']).
                            values(**account)
                    )
                    sess.execute(stmt)

    def insert_transactions(self):
        with self.session() as sess, sess.begin():
            for bank in banks:
                sess.add_all([Expenses(**row) for row in pydantic_validation_transactions(bank) if sess.execute(
                    select(Expenses).filter(
                        Expenses.transaction_id == row['transaction_id'])).scalars().first() is None])

                sess.add_all(
                    [Expenses_additional_info(**row) for row in pydantic_validation_transactions_additional_info(bank)
                     if sess.execute(
                        select(Expenses_additional_info).filter(
                            Expenses_additional_info.transaction_id == row[
                                'transaction_id'])).scalars().first() is None])


service = DB_service(banks, Session)
service.update_account_info()
