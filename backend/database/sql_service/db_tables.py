import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Float, Identity, LargeBinary, Date
from sqlalchemy.orm import declarative_base, relationship

base = declarative_base()

# Classes below represent our DB schema
class Users(base):
    __tablename__ = 'users'
    id: int = Column(Integer, Identity(start=1, cycle=True), primary_key=True)
    username: str = Column(String, unique=True)
    password: bytes = Column(LargeBinary)
    first_name: str = Column(String)
    last_name: str = Column(String)
    accounts=relationship("Accounts", back_populates="user")
    tokens=relationship("Tokens", back_populates="user")

class Accounts(base):
    __tablename__ = 'accounts'
    id: str = Column(String, primary_key=True)
    name: str = Column(String)
    balance: float = Column(Integer)
    subtype: str = Column(String, index=True)
    user_id=Column(Integer,ForeignKey("users.id"))
    bank_name=Column(String)
    expenses = relationship("Expenses", back_populates='account')
    user=relationship("Users", back_populates="accounts")


class Expenses(base):
    __tablename__ = 'expenses'
    transaction_id: str = Column(String, primary_key=True)
    created_date: datetime.date = Column(Date, default=None, index=True)
    amount: float = Column(Float)
    account_id: str = Column(String, ForeignKey('accounts.id'))
    expense_additional_info = relationship("Expenses_additional_info", back_populates='expense', uselist=False)
    account = relationship("Accounts", back_populates='expenses')


class Expenses_additional_info(base):
    __tablename__ = 'expenses_additional_info'
    transaction_id: str = Column(String, ForeignKey('expenses.transaction_id'), primary_key=True)
    category: str = Column(String, index=True)
    merchant_name: str = Column(String, index=True)
    expense = relationship("Expenses", back_populates='expense_additional_info', uselist=False)


class Tokens(base):
    __tablename__ = 'tokens'
    id: int = Column(Integer, Identity(start=1, cycle=True), primary_key=True)
    user_id: int = Column(Integer, ForeignKey('users.id'))
    bank_name: str = Column(String, nullable=False)
    token: str = Column(String, nullable=False)
    user = relationship("Users", back_populates="tokens")
