import pytest
from fastapi.testclient import TestClient
from app.schemas.user import UserCreate, UserRole
from fastapi import status


class TestAuthLogin:
    """Test cases for auth login endpoint."""
    
    async def test_login_success(self, client: TestClient, admin_user):
        """Test successful login."""
        print(f"Admin user created: {admin_user}")
        print(f"Admin user email: {admin_user.email}")
        print(f"Admin user username: {admin_user.username}")
        
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "admin@test.com",
                "password": "admin123"
            }
        )
        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.json()}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert "token_type" in data
        assert data["token_type"] == "bearer"
    
    async def test_login_invalid_credentials(self, client: TestClient):
        """Test login with invalid credentials."""
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "invalid@test.com",
                "password": "wrongpassword"
            }
        )
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Incorrect email/username or password" in response.json()["detail"]
    
    async def test_login_missing_email(self, client: TestClient):
        """Test login with missing email."""
        response = client.post(
            "/api/v1/auth/login",
            json={
                "password": "admin123"
            }
        )
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    async def test_login_missing_password(self, client: TestClient):
        """Test login with missing password."""
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "admin@test.com"
            }
        )
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
