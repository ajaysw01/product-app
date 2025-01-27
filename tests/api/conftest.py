import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.api.db import models  # Adjust the import
from src.api.db.database import Base
from fastapi.testclient import TestClient
from main import app

# Test database URL (use a separate test database for unit tests)
SQLALCHEMY_TEST_DATABASE_URL = "postgresql://postgres:root@localhost/test_db"

# Create engine and session for testing
engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create all tables in the test database
Base.metadata.create_all(bind=engine)

# Dependency override for testing
@pytest.fixture()
def db():
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()

# Create a TestClient instance for FastAPI
@pytest.fixture()
def client():
    client = TestClient(app)
    return client

# Optional: Clean up the database after each test
@pytest.fixture(scope="function")
def cleanup_db(db):
    yield db
    # Clean up the database after each test
    db.query(models.User).delete()  # Delete all users (or other entities)
    db.commit()

# Optional: Wrap each test in a transaction and rollback after
@pytest.fixture()
def db_session(db):
    db.begin()  # Start a transaction
    yield db
    db.rollback()  # Rollback any changes made during the test
