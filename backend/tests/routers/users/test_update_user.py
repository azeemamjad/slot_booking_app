import pytest
from fastapi.testclient import TestClient
from fastapi import status


class TestUpdateUser:
    """Test cases for update user endpoint."""
    
    def test_update_user_own_profile(self, client: TestClient, user_headers, normal_user):
        """Test user can update their own profile."""
        response = client.put(
            f"/api/v1/users/{normal_user.id}",
            headers=user_headers,
            json={
                "description": "Updated description"
            }
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["description"] == "Updated description"
    
    def test_update_user_admin_can_update_any(self, client: TestClient, admin_headers, normal_user):
        """Test admin can update any user's profile."""
        response = client.put(
            f"/api/v1/users/{normal_user.id}",
            headers=admin_headers,
            json={
                "description": "Admin updated description"
            }
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["description"] == "Admin updated description"
    
    def test_update_user_user_cannot_update_other(self, client: TestClient, user_headers, admin_user):
        """Test normal user cannot update other user's profile."""
        response = client.put(
            f"/api/v1/users/{admin_user.id}",
            headers=user_headers,
            json={
                "description": "Unauthorized update"
            }
        )
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_update_user_not_found(self, client: TestClient, admin_headers):
        """Test update non-existent user."""
        response = client.put(
            "/api/v1/users/999",
            headers=admin_headers,
            json={
                "description": "Update"
            }
        )
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_update_user_unauthorized(self, client: TestClient, normal_user):
        """Test unauthorized access to update user."""
        response = client.put(
            f"/api/v1/users/{normal_user.id}",
            json={
                "description": "Update"
            }
        )
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
