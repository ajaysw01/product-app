from fastapi.testclient import TestClient
from main import app
from src.api.db import models
import pytest
import uuid

client = TestClient(app)

# Importing db from conftest.py, it will be automatically available because pytest automatically loads fixtures from conftest.py
# No need to redefine the db fixture here

def get_token():
    response = client.post(
        "/login",
        data={"username": "john@example.com", "password": "testpassword"}
    )
    assert response.status_code == 200  # Ensure login is successful
    return response.json()["access_token"]

def test_login(db):
    user = models.User(name="John", email="john@example.com", password="testpassword")
    db.add(user)
    db.commit()
    db.refresh(user)
    
    response = client.post(
        "/login", 
        data={"username": "john@example.com", "password": "testpassword"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_protected_route(db):
    unique_email = f"john{uuid.uuid4()}@example.com"  # Ensure unique email
    user = models.User(name="Alice", email=unique_email, password="testpassword")
    db.add(user)
    db.commit()
    db.refresh(user)
 
    # Get token for authentication
    token = get_token()  
    response = client.get(
        f"/user/{user.id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    user_data = response.json()
    assert user_data["email"] == unique_email
    assert user_data["name"] == "Alice"
