from sqlmodel import SQLModel, Session, create_engine

from models import Customer
import json

# Database setup
database_name = "bank.db"
database_url = f"sqlite:///{database_name}"
initial_deposit = 100

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

# create database only when run from main
if __name__ == "__main__":
    SQLModel.metadata.create_all(engine)
    load_faithful_customers()