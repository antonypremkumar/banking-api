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