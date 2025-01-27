import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
from ...api.repo import userrepository
from ...api.db import models
from ...api.utils import schemas
from ...api.utils import hashing

# Fixtures for mock DB and user data
@pytest.fixture
def mock_db():
    return MagicMock()

@pytest.fixture
def fake_user_data():
    return schemas.User(name="Test User", email="test@example.com", password="testpassword")

@pytest.fixture
def mock_user_model():
    return MagicMock(spec=models.User)

# Test: Create User
def test_create_user(mock_db, fake_user_data):
    mock_db.query.return_value.filter.return_value.first.return_value = None  # Simulate no existing user
    user = userrepository.create(fake_user_data, mock_db)

    # Check if the user creation and database interactions are correct
    mock_db.add.assert_called_once_with(user)
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(user)
    
    # Check user attributes
    assert user.name == fake_user_data.name
    assert user.email == fake_user_data.email
    assert user.password != fake_user_data.password  # Password should be hashed

# Test: Show User
def test_show_user(mock_db, mock_user_model):
    mock_db.query.return_value.filter.return_value.first.return_value = mock_user_model
    user = userrepository.show(1, mock_db)

    assert user == mock_user_model

# Test: Delete User
def test_delete_user(mock_db, mock_user_model, fake_user_data):
    mock_db.query.return_value.filter.return_value.first.return_value = mock_user_model
    result = userrepository.delete(1, mock_db, fake_user_data)

    mock_db.delete.assert_called_once_with(mock_user_model)
    mock_db.commit.assert_called_once()
    assert result == {"message": "User deleted successfully"}

# Test: Update User
def test_update_user(mock_db, mock_user_model, fake_user_data):
    mock_db.query.return_value.filter.return_value.first.return_value = mock_user_model
    update_data = schemas.UserUpdateModel(name="Updated Name")
    updated_user = userrepository.update(1, update_data, mock_db, fake_user_data)

    assert updated_user.name == "Updated Name"
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(mock_user_model)
