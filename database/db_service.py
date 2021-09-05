import datetime
from typing import List

from database.db_tables import Accounts, Expenses
from database.pydantic_models import Expenses_pydantic, Accounts_pydantic
from plaid_service.plaid_dashboard import plaid_service
from session import Session

banks = ["amex", "navy", "chase"]


class Accounts_operations():
    def accounts_update(self, session: Session, banks: List):
        records = [plaid_service.get_acounts_info(bank)['accounts'] for bank in banks]

        # inserting new accounts into database
        [session.add(Accounts(**Accounts_pydantic(**record).to_dict())) for row in records for record in row
         if session.query(Accounts).filter(Accounts.id == record["account_id"]).first() is None]

        # updating amount for existing accounts
        [session.query(Accounts).filter(Accounts.id == Accounts_pydantic(**record).id).update(
            {Accounts.balance: Accounts_pydantic(**record).balance}) for row in records for record in row]
        session.commit()


class Expenses_operations():
    def transactions_update(self, session: Session, from_date: datetime.date, banks):
        records = [plaid_service.get_transactions(bank, from_date, datetime.date.today())["transactions"] for bank in
                   banks]
        [session.add(Expenses(**Expenses_pydantic(**transaction).dict())) for record in records for transaction in
         record
         if session.query(Expenses).filter(Expenses.transaction_id == transaction["transaction_id"]).first() is None]
        session.commit()


accounts = Accounts_operations()
expenses = Expenses_operations()

with Session() as sess:
    accounts.accounts_update(sess, banks)
