from session_sql import Session
from database.db_service import pydantic_validation_transactions, pydantic_validation_transactions_additional_info, pydantic_validation_accounts
from db_tables import Expenses,Expenses_additional_info,Accounts

banks=['amex','bofa','chase','navy']

with Session() as sess:
    with sess.begin():
        for bank in banks:
            for row in pydantic_validation_transactions(bank):
                expense=Expenses(**row)
                print(expense.expense_additional_info)
            for row in pydantic_validation_transactions_additional_info(bank):
                add_info=Expenses_additional_info(**row)
                print(add_info.expense)
            expense.expense_additional_info=add_info
            sess.add(expense)
            # for row in pydantic_validation_accounts(bank):
            #     sess.add(Accounts(**row))

