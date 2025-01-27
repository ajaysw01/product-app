from src.api.repo import userrepository
from src.api.db import models
from src.api.utils import schemas
from sqlalchemy.orm import Session
import pytest
from ..conftest import get_db
from src.api.utils.hashing import Hash

@pytest.fixture
def db():
    db = get_db()
    try:
        yield db
    finally:
        db.close()

def test_create_user(db: Session):
    request = schemas.User(
        name="John Doe", email="john@example.com", password="testpassword"
    )

    created_user = userrepository.create(request, db)

    assert created_user.name == "John Doe"
    assert created_user.email == "john@example.com"
    # Ensure password is hashed and valid
    assert created_user.password != "testpassword"
    assert Hash.verify("testpassword", created_user.password)

def test_show_user(db: Session):
    user = models.User(name="Jane Doe", email="jane@example.com", password="testpassword")
    db.add(user)
    db.commit()
    db.refresh(user)
    fetched_user = userrepository.show(user.id, db)
    assert fetched_user.name == "Jane Doe"
    assert fetched_user.email == "jane@example.com"

def test_update_user(db: Session):
    user = models.User(name="Old Name", email="old@example.com", password="testpassword")
    db.add(user)
    db.commit()
    db.refresh(user)
    update_request = schemas.UserUpdateModel(name="New Name")
    updated_user = userrepository.update(user.id, update_request, db, user)
    assert updated_user.name == "New Name"

def test_delete_user(db: Session):
    user = models.User(name="Delete User", email="delete@example.com", password="testpassword")
    db.add(user)
    db.commit()
    db.refresh(user)
    response = userrepository.delete(user.id, db, user)
    assert response["message"] == "User deleted successfully"
    deleted_user = db.query(models.User).filter(models.User.id == user.id).first()
    assert deleted_user is None
