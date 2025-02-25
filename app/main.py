from fastapi import FastAPI, status
from fastapi.responses import HTMLResponse
from fastapi.exceptions import HTTPException

from sqlmodel import Session, select
from database import engine, initial_deposit
import uvicorn

from os import environ
from models import CustomerBase, Customer, BankAccount, Transfer
from typing import List

app = FastAPI()
session = Session(bind=engine)

#routes
# a simple HTML response
@app.get('/', response_class=HTMLResponse)
async def home():
    return '''
    <h1> Welcome to Antony's bank </h1>
    '''

# a java script response for basic information
@app.get('/info')
def info():
    return {
        'version': "0.1.0",
        'user': environ['USER']
    }

# add a customer
@app.post('/customer', status_code=status.HTTP_201_CREATED)
async def add_a_customer(customer: CustomerBase):
    new_customer = Customer(name=customer.name)
    with Session(engine) as session:
        statement = select(Customer).where(Customer.name == customer.name)
        if session.exec(statement).one_or_none():
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="customer name already in use")
        session.add(new_customer)
        session.commit()
        session.refresh(new_customer)
    return new_customer

# get all customers
@app.get('/customer', response_model=List[Customer])
async def get_all_customers():
    with Session(engine) as session:
        statement=select(Customer)
        result=session.exec(statement)
        all_customers=result.all()
        # error handling could be done here
    return all_customers

# add an account to a customer
@app.post('/account/{customer_id}', status_code=status.HTTP_201_CREATED)
async def add_an_account(customer_id: int):
    new_account = BankAccount(customer_id=customer_id, balance=initial_deposit)
    with Session(engine) as session:
        customer = session.get(Customer, customer_id)
        if not customer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
        session.add(new_account)
        session.commit()
        session.refresh(new_account)
    return {"message": f"Added an account successfully to {customer_id}"}

# get balance
@app.get('/balance/{account_id}', response_model=int)
async def get_balance(account_id: int):
    with Session(engine) as session:
        account = session.get(BankAccount, account_id)
        if not account:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    return account.balance

# get balances
@app.get('/balances/{customer_id}', response_model=List[BankAccount])
async def get_balances(customer_id: int):
    with Session(engine) as session:
        # check if customer exists
        customer = session.get(Customer, customer_id)
        if not customer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

        statement = select(BankAccount).where(BankAccount.customer_id == customer_id)
        result=session.exec(statement)
        all_accounts=result.all()
    return all_accounts

# transfer a specific account between accounts
@app.post("/transfer/{from_account_id}/{to_account_id}/{amount}") # A class for a successful response could be added
def transfer_funds(from_account_id: int, to_account_id: int, amount: float):
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Transfer amount must be positive")
    
    with Session(engine) as session:
        from_account = session.get(BankAccount, from_account_id)
        to_account = session.get(BankAccount, to_account_id)
    
        if not from_account or not to_account:
            raise HTTPException(status_code=404, detail="One or both accounts not found")
    
        if from_account.balance < amount:
            raise HTTPException(status_code=400, detail="Insufficient funds")
    
        from_account.balance -= amount
        to_account.balance += amount

        session.add(from_account)
        session.commit()
        session.refresh(from_account)
    
        session.add(to_account)
        session.commit()
        session.refresh(to_account)
    
        new_transfer = Transfer(from_account_id=from_account_id, to_account_id=to_account_id, amount=amount)
        session.add(new_transfer)
        session.commit()
        session.refresh(new_transfer)
    return {"message": "Transfer successful"}

# account statement of records
@app.get("/account/{account_id}/transfers", response_model=List[Transfer])
def get_transfer_history(account_id: int):
    with Session(engine) as session:
        # check if account exists
        account = session.get(BankAccount, account_id)
        if not account:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")

        statement = select(Transfer).where((Transfer.from_account_id == account_id) | (Transfer.to_account_id == account_id))
        transfers = session.exec(statement).all()
    return transfers

if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=8000)