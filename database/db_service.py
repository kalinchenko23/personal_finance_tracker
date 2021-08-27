import datetime

from sqlalchemy.orm import query

from database.db_tables import Accounts, Expenses
from plaid_service.plaid_dashboard import plaid_service
from session import Session, engine
from sqlalchemy import select, column, func, table, update


class Accounts_operations():
    def original_insertion(self):
        banks = ["amex", "navy", "chase"]
        records = [plaid_service.get_acounts_info(bank) for bank in banks]
        accoounts = [Accounts(id=record["account_id"], name=record["name"], balance=record["balances"]["current"],
                              subtype=str(record["subtype"])) for row in records for record in row]
        return accoounts

    def update_balance(self, session: Session):
        banks = ["amex", "navy", "chase"]
        records = [plaid_service.get_acounts_info(bank) for bank in banks]
        result = [session.query(Accounts).filter(Accounts.id == record["account_id"]).update(
            {Accounts.balance: record["balances"]["current"]}) for row in records for record in row]
        return result


class Expenses_operations():
    def transactions_update(self, session: Session):
        banks = ["amex", "navy", "chase"]
        records = [plaid_service.get_transactions(bank, datetime.date(2021, 1, 1), datetime.date.today()) for bank in
                   banks]
        transactions = [Expenses(created_date=record["date"], amount=str(record["amount"]), category=record["category"],
                                 merchant_name=record["merchant_name"],
                                 transaction_id=record["transaction_id"], account_id=record["account_id"]) for row in
                        records for record in row if session.query(Expenses).filter(Expenses.transaction_id == record["transaction_id"]).first() is None]
        [session.add(transaction) for transaction in transactions]
        session.commit()



accounts = Accounts_operations()
expenses = Expenses_operations()

with Session() as sess:
    expenses.transactions_update(sess)