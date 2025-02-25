from fastapi import FastAPI, status
from fastapi.responses import HTMLResponse
from fastapi.exceptions import HTTPException

from sqlmodel import Session, select
from database import engine
import uvicorn

from os import environ
from models import CustomerBase, Customer
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
        all_categories=result.all()
        # error handling could be done here
    return all_categories

if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=8000)