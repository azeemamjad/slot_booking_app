import pytest
from fastapi.testclient import TestClient
from app.schemas.user import UserCreate, UserRole


class TestAuthRegister:
    """Test cases for auth register endpoint."""
    
    async def test_register_success(self, client: TestClient):
        """Test successful user registration."""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "newuser@test.com",
                "username": "newuser",
                "password": "newuser123",
                "role": "normal",
                "department_id": 1
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "newuser@test.com"
        assert data["username"] == "newuser"
        assert data["role"] == "normal"
        assert "id" in data
    
    async def test_register_duplicate_email(self, client: TestClient, admin_user):
        """Test registration with duplicate email."""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "admin@test.com",
                "username": "newuser",
                "password": "newuser123",
                "role": "normal",
                "department_id": 1
            }
        )
        
        assert response.status_code == 400
        assert "Email already registered" in response.json()["detail"]
    
    async def test_register_duplicate_username(self, client: TestClient, admin_user):
        """Test registration with duplicate username."""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "newuser@test.com",
                "username": "admin",
                "password": "newuser123",
                "role": "normal",
                "department_id": 1
            }
        )
        
        assert response.status_code == 400
        assert "Username already taken" in response.json()["detail"]
    
    async def test_register_missing_required_fields(self, client: TestClient):
        """Test registration with missing required fields."""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "newuser@test.com",
                "password": "newuser123"
            }
        )
        
        assert response.status_code == 422
    
    async def test_register_invalid_email(self, client: TestClient):
        """Test registration with invalid email format."""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "invalid-email",
                "username": "newuser",
                "password": "newuser123",
                "role": "normal",
                "department_id": 1
            }
        )
        
        assert response.status_code == 422
