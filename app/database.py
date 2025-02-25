from sqlmodel import SQLModel, Session, create_engine

# Database setup
database_name = "bank.db"
database_url = f"sqlite:///{database_name}"
initial_deposit = 100

engine = create_engine(database_url, echo=True)

# create database only when run from main
if __name__ == "__main__":
    SQLModel.metadata.create_all(engine)