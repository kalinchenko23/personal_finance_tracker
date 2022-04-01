from sqlalchemy import select

import sqlalchemy

from session_sql import Session
from database.db_service import pydantic_validation_transactions, pydantic_validation_transactions_additional_info, \
    pydantic_validation_accounts
from db_tables import Expenses, Expenses_additional_info, Accounts

banks = ['amex', 'bofa', 'chase', 'navy']


class DB_service():
    def __init__(self, banks,session):
        self.banks = banks
        self.session=session

    def insert_account_info(self):
        with self.session() as sess, sess.begin():
            for bank in self.banks:
                sess.add(Accounts(**pydantic_validation_accounts(bank)))
    def insert_transactions(self):
        with self.session() as sess:
            for bank in self.banks:
                most_recent_date = sess.execute(select(Expenses).order_by(Expenses.created_date.desc())).scalars().first().created_date
                for row in pydantic_validation_transactions(bank):
                    expense = Expenses(**row)
                    sess.add(expense)
                try:
                    sess.commit()
                except Exception as exc:
                    print(f'{exc.__context__}')
                    pass
                finally:
                    sess.close()

    def insert_additional_info(self):
        with self.session() as sess:
            for bank in self.banks:
                for row in pydantic_validation_transactions_additional_info(bank):
                    additional_info = Expenses_additional_info(**row)
                    sess.add(additional_info)
                try:
                    sess.commit()
                except Exception as exc:
                    print(f'{exc.__context__}')
                    pass
                finally:
                    sess.close()






service = DB_service(banks,Session)
service.insert_transactions()

