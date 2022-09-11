import sys
sys.path.insert(0, '/Users/maximkalinchenko/Desktop/personal_finance_tracker/backend/plaid_service')
sys.path.insert(1, '/Users/maximkalinchenko/Desktop/personal_finance_tracker/backend/database')
sys.path.insert(2, '/Users/maximkalinchenko/Desktop/personal_finance_tracker/backend/database/fastapi_sql')
from fastapi import FastAPI, Query
import uvicorn
from plaid_dashboard import plaid_service
from pydantic_models import Accounts_pydantic
from pydantic import BaseModel
from fastapi_sql_service import User
data=plaid_service.get_acounts_info
app = FastAPI()

@app.post('/bank_info/')
def test(bank_info: Accounts_pydantic, q : str =Query(max_length=2) ):
    return data(bank_info.name)[0]

# @app.post('/users/')
# uvicorn.run(app)