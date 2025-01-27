from fastapi.testclient import TestClient
from main import app  
from tests.api.auth.test_authentication import get_token
from src.api.db import models
from ..conftest import get_db
from sqlalchemy.orm import Session
import pytest

client = TestClient(app)

@pytest.fixture
def db():
    db = get_db()  # Ensure you have a session provided for your tests
    try:
        yield db
    finally:
        db.close()

# Create user via the route and test the response
def test_create_user_route(db: Session):
    token = get_token()  
    response = client.post(
        "/user/",
        json={"name": "Alice", "email": "alice@example.com", "password": "testpassword"},
        headers={"Authorization": f"Bearer {token}"}  # Include the token in the header
    )
    assert response.status_code == 201
    created_user = db.query(models.User).filter(models.User.email == "alice@example.com").first()
    assert created_user is not None
    assert created_user.name == "Alice"
    assert created_user.email == "alice@example.com"
    # Ensure the password is hashed
    assert created_user.password != "testpassword"

# Test getting a user by ID
def test_get_user_route(db: Session):
    # Pre-create a user in the database to test the GET request
    user = models.User(name="Bob", email="bob@example.com", password="testpassword")
    db.add(user)
    db.commit()
    db.refresh(user)
    
    token = get_token()  # Retrieve the token
    
    response = client.get(
        f"/user/{user.id}",  # Fetch the created user's ID
        headers={"Authorization": f"Bearer {token}"}  # Include the token in the header
    )
    
    assert response.status_code == 200
    user_data = response.json()
    assert user_data["name"] == "Bob"
    assert user_data["email"] == "bob@example.com"
