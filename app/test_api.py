from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from main import app
import pytest
from models import Customer, BankAccount

@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[Session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

def test_add_customer(client: TestClient):
    response = client.post("/customer", json={"name": "Antony Premkumar"})
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "Antony Premkumar"
    assert "id" in data

def test_add_duplicate_customer(client: TestClient):
    client.post("/customer", json={"name": "Antony Premkumar"})
    response = client.post("/customer", json={"name": "Antony Premkumar"})
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()["detail"] == "customer name already in use"

def test_add_account(client: TestClient, session: Session):
    customer_id=5
    
    response = client.post(f"/account/{customer_id}")
    assert response.status_code == status.HTTP_201_CREATED

def test_get_balance(client: TestClient, session: Session):
    account_id=2

    response = client.get(f"/balance/{account_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == 10000

def test_transfer_funds(client: TestClient, session: Session):
    account1_id=1
    account2_id=5

    response = client.post(f"/transfer/{account1_id}/{account2_id}/300")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Transfer successful"}

    response = client.get(f"/balance/{account1_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == 9700

    response = client.get(f"/balance/{account2_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == 10300

def test_get_transfer_history(client: TestClient, session: Session):
    account1_id=5
    account2_id=2

    response = client.post(f"/transfer/{account1_id}/{account2_id}/500")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Transfer successful"}

    response = client.get(f"/account/{account1_id}/transfers")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert len(data) == 2
    assert data[0]["from_account_id"] == 1
    assert data[0]["to_account_id"] == account1_id
    assert data[0]["amount"] == 300
    assert data[1]["from_account_id"] == account1_id
    assert data[1]["to_account_id"] == account2_id
    assert data[1]["amount"] == 500