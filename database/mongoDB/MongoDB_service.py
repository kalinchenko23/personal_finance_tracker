import mongoengine
from database.db_service import pydantic_validation_transactions, pydantic_validation_transactions_additional_info, \
    pydantic_validation_accounts, banks
from database.mongoDB.documents import Accounts, Expenses_additional_info, Expenses

mongoengine.connect(host="mongodb://personal_finanse_tracker_mongodb_1/personl_finanse_tracker")


# This function inserts and updates transactions and accounts
def inserting_transactions_updating_accounts():
    for bank in banks:
        transactions = [Expenses(**record) for record in pydantic_validation_transactions(bank)]
        additional_info = [Expenses_additional_info(category=record['category'], merchant_name=record['merchant_name'])
                           for record in
                           pydantic_validation_transactions_additional_info(bank)]
        account = Accounts(**pydantic_validation_accounts(bank))
        paird_transactions_and_info = list(map(lambda x, y: (x, y), transactions, additional_info))
        for pair in paird_transactions_and_info:
            transaction, additional_info = pair
            transaction.additional_info = additional_info
            transaction.save()
        account.save()


inserting_transactions_updating_accounts()
