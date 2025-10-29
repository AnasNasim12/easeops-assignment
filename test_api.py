import pytest
from fastapi.testclient import TestClient
from main import app
from database import get_db
from models import Base, User, Book
from auth_utils import get_password_hash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import settings

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="module")
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def test_user():
    return {
        "email": "test@example.com",
        "username": "testuser",
        "full_name": "Test User",
        "password": "password123"
    }

@pytest.fixture
def auth_headers(test_user, setup_database):
    # Register user
    response = client.post("/api/auth/register", json=test_user)
    assert response.status_code == 200
    
    # Login user
    login_data = {
        "username": test_user["username"],
        "password": test_user["password"]
    }
    response = client.post("/api/auth/login", json=login_data)
    assert response.status_code == 200
    
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "EaseOps E-Library User Backend API"

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_user_registration(test_user, setup_database):
    response = client.post("/api/auth/register", json=test_user)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user["email"]
    assert data["username"] == test_user["username"]

def test_user_login(test_user, setup_database):
    # Register user first
    client.post("/api/auth/register", json=test_user)
    
    # Login
    login_data = {
        "username": test_user["username"],
        "password": test_user["password"]
    }
    response = client.post("/api/auth/login", json=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_get_current_user(auth_headers):
    response = client.get("/api/auth/me", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"

def test_get_books():
    response = client.get("/api/library/books")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_categories():
    response = client.get("/api/library/categories")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_tags():
    response = client.get("/api/library/tags")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_user_profile(auth_headers):
    response = client.get("/api/users/profile", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"

def test_update_user_preferences(auth_headers):
    preferences = {
        "dark_mode": True,
        "email_notifications": False
    }
    response = client.put("/api/users/preferences", json=preferences, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Preferences updated successfully"

def test_get_faq():
    response = client.get("/api/interactions/faq")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_submit_contact_request():
    contact_data = {
        "name": "Test User",
        "email": "test@example.com",
        "subject": "Test Subject",
        "message": "Test message"
    }
    response = client.post("/api/interactions/contact", json=contact_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == contact_data["name"]

def test_unauthorized_access():
    response = client.get("/api/users/profile")
    assert response.status_code == 401

if __name__ == "__main__":
    pytest.main([__file__])
