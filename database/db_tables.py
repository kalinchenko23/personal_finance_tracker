import datetime

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates

from alembic.operations import Operations
from alembic.runtime.migration import MigrationContext
from sqlalchemy import Column, Integer, DateTime, String, ForeignKey, Float
from sqlalchemy.orm import declarative_base, relationship
from alembic import op

from session import Session, engine

base = declarative_base()

conn = engine.connect()
ctx = MigrationContext.configure(conn)
op = Operations(ctx)


class Expenses(base):
    __tablename__ = 'expenses'
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    created_date: datetime.datetime = Column(DateTime, default=None, index=True)
    amount: str = Column(Float)
    _category: str = Column(String, index=True)
    merchant_name: str = Column(String, index=True)
    transaction_id: str = Column(String)
    account_id: int = Column(String, ForeignKey('accounts.id'))
    accounts = relationship('Accounts', back_populates='transactions')

    @hybrid_property
    def category(self):
        return self._category

    @category.setter
    def category(self, category):
        self._category = category[-1]


class Accounts(base):
    __tablename__ = 'accounts'
    id: int = Column(String, primary_key=True)
    name: str = Column(String)
    balance: str = Column(Integer)
    subtype: str = Column(String, index=True)
    transactions = relationship("Expenses", back_populates='accounts')


def create_tables():
    base.metadata.create_all(engine)


create_tables()
