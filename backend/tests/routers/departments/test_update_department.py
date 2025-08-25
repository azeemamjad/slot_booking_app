import pytest
from fastapi.testclient import TestClient
from fastapi import status


class TestUpdateDepartment:
    """Test cases for update department endpoint."""
    
    def test_update_department_admin_success(self, client: TestClient, admin_headers):
        """Test admin can update department."""
        # First create a department
        create_response = client.post(
            "/api/v1/departments/",
            headers=admin_headers,
            json={
                "title": "Original Department",
                "description": "Original description"
            }
        )
        department_id = create_response.json()["id"]
        
        response = client.put(
            f"/api/v1/departments/{department_id}",
            headers=admin_headers,
            json={
                "title": "Updated Department",
                "description": "Updated description"
            }
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["title"] == "Updated Department"
        assert data["description"] == "Updated description"
    
    def test_update_department_user_forbidden(self, client: TestClient, user_headers, admin_headers):
        """Test normal user cannot update departments."""
        # First create a department as admin
        create_response = client.post(
            "/api/v1/departments/",
            headers=admin_headers,
            json={
                "title": "Test Department Update",
                "description": "Test description"
            }
        )
        department_id = create_response.json()["id"]
        
        response = client.put(
            f"/api/v1/departments/{department_id}",
            headers=user_headers,
            json={
                "title": "Unauthorized Update"
            }
        )
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_update_department_not_found(self, client: TestClient, admin_headers):
        """Test update non-existent department."""
        response = client.put(
            "/api/v1/departments/999",
            headers=admin_headers,
            json={
                "title": "Update"
            }
        )
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_update_department_unauthorized(self, client: TestClient):
        """Test unauthorized access to update department."""
        response = client.put(
            "/api/v1/departments/1",
            json={
                "title": "Update"
            }
        )
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
