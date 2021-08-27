from alembic.operations import Operations
from alembic.runtime.migration import MigrationContext
from sqlalchemy import Column, String, ForeignKey, Integer

from database.session import engine

conn = engine.connect()
ctx = MigrationContext.configure(conn)
op = Operations(ctx)

#This file is used to modify a state of database schema, you can
#add new function as needed using https://alembic.sqlalchemy.org/en/latest/ops.html documentation

def add_column(table_name: str, column: Column):
    op.add_column(table_name=table_name, column=column)

def drop_column(table_name: str, column_name: str):
    op.drop_column(table_name, column_name)

def alter_table_multiple_statements():
    with op.batch_alter_table("expenses") as batch_op:
        batch_op.add_column(Column('test_column',String))
        batch_op.drop_column('test_column')

add_column('expenses',Column("account_id",Integer,ForeignKey('accounts.id')))