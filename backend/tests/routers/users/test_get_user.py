import pytest
from fastapi.testclient import TestClient
from fastapi import status

class TestGetUser:
    """Test cases for get specific user endpoint."""
    
    def test_get_user_own_profile(self, client: TestClient, user_headers, normal_user):
        """Test user can get their own profile."""
        response = client.get(f"/api/v1/users/{normal_user.id}", headers=user_headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == normal_user.id
        assert data["email"] == normal_user.email
    
    def test_get_user_admin_can_get_any(self, client: TestClient, admin_headers, normal_user):
        """Test admin can get any user's profile."""
        response = client.get(f"/api/v1/users/{normal_user.id}", headers=admin_headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == normal_user.id
    
    def test_get_user_user_cannot_get_other(self, client: TestClient, user_headers, admin_user):
        """Test normal user cannot get other user's profile."""
        response = client.get(f"/api/v1/users/{admin_user.id}", headers=user_headers)
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_get_user_not_found(self, client: TestClient, admin_headers):
        """Test get non-existent user."""
        response = client.get("/api/v1/users/999", headers=admin_headers)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_get_user_unauthorized(self, client: TestClient, normal_user):
        """Test unauthorized access to get user."""
        response = client.get(f"/api/v1/users/{normal_user.id}")
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
