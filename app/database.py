from sqlmodel import SQLModel, Session, create_engine, select

from models import Customer, BankAccount
import json

# Database setup
database_name = "bank.db"
database_url = f"sqlite:///{database_name}"
initial_deposit = 10000 # in cents is better for computer arithmetic

engine = create_engine(database_url, echo=True)

# Load predefined customers
def load_faithful_customers():
    with open("faithful_customers.json", "r") as file:
        customers = json.load(file)
    with Session(engine) as session:
        for customer in customers:
            if not session.get(Customer, customer["id"]):
                session.add(Customer(id=customer["id"], name=customer["name"]))
        session.commit()

# Give every customer a bank account
def create_account_for_faithful_customers():
    with Session(engine) as session:
        statement=select(Customer)
        result=session.exec(statement)
        all_customers=result.all()

        for customer in all_customers:
            account = BankAccount(customer_id=customer.id, balance=initial_deposit)
            session.add(account)
            session.commit()
            session.refresh(account)

# create database only when run from main
if __name__ == "__main__":
    SQLModel.metadata.create_all(engine)
    load_faithful_customers()
    create_account_for_faithful_customers()