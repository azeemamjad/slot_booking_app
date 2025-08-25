import pytest
from fastapi.testclient import TestClient
from fastapi import status


class TestDeleteDepartment:
    """Test cases for delete department endpoint."""
    
    def test_delete_department_admin_success(self, client: TestClient, admin_headers):
        """Test admin can delete department."""
        # First create a department
        create_response = client.post(
            "/api/v1/departments/",
            headers=admin_headers,
            json={
                "title": "Department to Delete",
                "description": "Will be deleted"
            }
        )
        department_id = create_response.json()["id"]
        
        response = client.delete(
            f"/api/v1/departments/{department_id}",
            headers=admin_headers
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "message" in data
        assert "deleted successfully" in data["message"]
    
    def test_delete_department_user_forbidden(self, client: TestClient, user_headers, admin_headers):
        """Test normal user cannot delete departments."""
        # First create a department as admin
        create_response = client.post(
            "/api/v1/departments/",
            headers=admin_headers,
            json={
                "title": "Test Department Forbidden",
                "description": "Test description"
            }
        )
        department_id = create_response.json()["id"]
        
        response = client.delete(
            f"/api/v1/departments/{department_id}",
            headers=user_headers
        )
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_delete_department_not_found(self, client: TestClient, admin_headers):
        """Test delete non-existent department."""
        response = client.delete(
            "/api/v1/departments/999",
            headers=admin_headers
        )
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_delete_department_unauthorized(self, client: TestClient):
        """Test unauthorized access to delete department."""
        response = client.delete("/api/v1/departments/1")
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
