import pytest
from fastapi.testclient import TestClient
from fastapi import status


class TestCreateUser:
    """Test cases for create user endpoint."""
    
    def test_create_user_admin_success(self, client: TestClient, admin_headers):
        """Test admin can create user."""
        response = client.post(
            "/api/v1/users/",
            headers=admin_headers,
            json={
                "email": "newuser@test.com",
                "username": "newuser",
                "password": "newuser123",
                "role": "normal",
                "department_id": 1
            }
        )
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["email"] == "newuser@test.com"
        assert data["username"] == "newuser"
        assert data["role"] == "normal"
        assert "id" in data
    
    def test_create_user_user_forbidden(self, client: TestClient, user_headers):
        """Test normal user cannot create users."""
        response = client.post(
            "/api/v1/users/",
            headers=user_headers,
            json={
                "email": "newuser@test.com",
                "username": "newuser",
                "password": "newuser123",
                "role": "normal",
                "department_id": 1
            }
        )
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_create_user_duplicate_email(self, client: TestClient, admin_headers, admin_user):
        """Test create user with duplicate email."""
        response = client.post(
            "/api/v1/users/",
            headers=admin_headers,
            json={
                "email": "admin@test.com",
                "username": "newuser",
                "password": "newuser123",
                "role": "normal",
                "department_id": 1
            }
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Email already registered" in response.json()["detail"]
    
    def test_create_user_duplicate_username(self, client: TestClient, admin_headers, admin_user):
        """Test create user with duplicate username."""
        response = client.post(
            "/api/v1/users/",
            headers=admin_headers,
            json={
                "email": "newuser@test.com",
                "username": "admin",
                "password": "newuser123",
                "role": "normal",
                "department_id": 1
            }
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Username already taken" in response.json()["detail"]
    
    def test_create_user_unauthorized(self, client: TestClient):
        """Test unauthorized access to create user."""
        response = client.post(
            "/api/v1/users/",
            json={
                "email": "newuser@test.com",
                "username": "newuser",
                "password": "newuser123",
                "role": "normal",
                "department_id": 1
            }
        )
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
