import datetime
from sqlalchemy import Column, Integer, DateTime, String, ForeignKey, Float
from sqlalchemy.orm import declarative_base, relationship


base = declarative_base()

class Expenses(base):
    __tablename__ = 'expenses'
    transaction_id: str = Column(String, primary_key=True)
    created_date: datetime.datetime = Column(DateTime, default=None, index=True)
    amount: float = Column(Float)
    merchant_name: str = Column(String, index=True)
    expense_additional_info = relationship("Expenses_additional_info", back_populates='expense', uselist=False)


class Expenses_additional_info(base):
    __tablename__ = 'expenses_additional_info'
    transaction_id: str = Column(String, ForeignKey('expenses.transaction_id'),primary_key=True)
    category: str = Column(String, index=True)
    account_id: str = Column(String, ForeignKey('accounts.id'))
    expense=relationship("Expenses",back_populates='expense_additional_info',uselist=False)
    account=relationship("Accounts",back_populates='expense_additional_info')

#
class Accounts(base):
    __tablename__ = 'accounts'
    id: str = Column(String,primary_key=True)
    name: str = Column(String)
    balance: float = Column(Integer)
    subtype: str = Column(String, index=True)
    expense_additional_info=relationship("Expenses_additional_info",back_populates='account')
