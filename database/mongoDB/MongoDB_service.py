import time, sys
sys.path.insert(1,'/Users/maximkalinchenko/Desktop/personal_finance_tracker/database')
sys.path.insert(1,'/Users/maximkalinchenko/Desktop/personal_finance_tracker/logging_service')
import mongoengine
from db_service import pydantic_validation_transactions, pydantic_validation_transactions_additional_info, \
    pydantic_validation_accounts, banks
from mongoDB.documents import Accounts, Expenses_additional_info, Expenses
from logger import finance_logger

mongoengine.connect('personal_finance_tracker')
# This function inserts and updates transactions and accounts

def inserting_transactions_updating_accounts():
    for bank in banks:
        transactions = [Expenses(**record) for record in pydantic_validation_transactions(bank)]
        additional_info = [Expenses_additional_info(category=record['category'], merchant_name=record['merchant_name'])
                           for record in
                           pydantic_validation_transactions_additional_info(bank)]
        paird_transactions_and_info = list(map(lambda x, y: (x, y), transactions, additional_info))
        for pair in paird_transactions_and_info:
            transaction, additional_info = pair
            transaction.additional_info = additional_info
            try:
                transaction.save()
            except Exception as ex:
                finance_logger.debug("Exception occured", exc_info=True)
        #Here we are updating accounts
        accounts = pydantic_validation_accounts(bank)
        for instance in accounts:
            account = Accounts(**instance)
            account.save()
        finance_logger.info(f"Transactions for {bank} are updated")


inserting_transactions_updating_accounts()