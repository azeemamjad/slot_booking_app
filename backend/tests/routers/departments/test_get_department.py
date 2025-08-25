import pytest
from fastapi.testclient import TestClient
from fastapi import status


class TestGetDepartment:
    """Test cases for get specific department endpoint."""
    
    def test_get_department_success(self, client: TestClient, user_headers, admin_headers):
        """Test get specific department."""
        # First create a department as admin
        create_response = client.post(
            "/api/v1/departments/",
            headers=admin_headers,
            json={
                "title": "Test Department Get",
                "description": "Test description"
            }
        )
        department_id = create_response.json()["id"]
        
        response = client.get(f"/api/v1/departments/{department_id}", headers=user_headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == department_id
        assert data["title"] == "Test Department Get"
    
    def test_get_department_not_found(self, client: TestClient, user_headers):
        """Test get non-existent department."""
        response = client.get("/api/v1/departments/999", headers=user_headers)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_get_department_unauthorized(self, client: TestClient):
        """Test unauthorized access to get department."""
        response = client.get("/api/v1/departments/1")
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
