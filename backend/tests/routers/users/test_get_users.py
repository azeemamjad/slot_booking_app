import pytest
from fastapi.testclient import TestClient
from fastapi import status


class TestGetUsers:
    """Test cases for get users endpoint."""
    
    def test_get_users_admin_success(self, client: TestClient, admin_headers):
        """Test admin can get all users."""
        response = client.get("/api/v1/users/", headers=admin_headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1  # At least admin user
    
    def test_get_users_user_forbidden(self, client: TestClient, user_headers):
        """Test normal user cannot get all users."""
        response = client.get("/api/v1/users/", headers=user_headers)
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_get_users_unauthorized(self, client: TestClient):
        """Test unauthorized access to get users."""
        response = client.get("/api/v1/users/")
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_get_users_with_pagination(self, client: TestClient, admin_headers):
        """Test get users with pagination parameters."""
        response = client.get(
            "/api/v1/users/?skip=0&limit=10",
            headers=admin_headers
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) <= 10
