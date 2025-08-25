import pytest
from fastapi.testclient import TestClient
from fastapi import status


class TestDeleteUser:
    """Test cases for delete user endpoint."""
    
    def test_delete_user_admin_success(self, client: TestClient, admin_headers, normal_user):
        """Test admin can delete user."""
        response = client.delete(
            f"/api/v1/users/{normal_user.id}",
            headers=admin_headers
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "message" in data
        assert "deleted successfully" in data["message"]
    
    def test_delete_user_user_forbidden(self, client: TestClient, user_headers, normal_user):
        """Test normal user cannot delete users."""
        response = client.delete(
            f"/api/v1/users/{normal_user.id}",
            headers=user_headers
        )
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_delete_user_not_found(self, client: TestClient, admin_headers):
        """Test delete non-existent user."""
        response = client.delete(
            "/api/v1/users/999",
            headers=admin_headers
        )
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_delete_user_unauthorized(self, client: TestClient, normal_user):
        """Test unauthorized access to delete user."""
        response = client.delete(f"/api/v1/users/{normal_user.id}")
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
