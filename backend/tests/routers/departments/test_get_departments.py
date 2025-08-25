import pytest
from fastapi.testclient import TestClient
from fastapi import status


class TestGetDepartments:
    """Test cases for get departments endpoint."""
    
    def test_get_departments_success(self, client: TestClient, user_headers):
        """Test get all departments."""
        response = client.get("/api/v1/departments/", headers=user_headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_departments_with_pagination(self, client: TestClient, user_headers):
        """Test get departments with pagination."""
        response = client.get(
            "/api/v1/departments/?skip=0&limit=10",
            headers=user_headers
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) <= 10
    
    def test_get_departments_unauthorized(self, client: TestClient):
        """Test unauthorized access to get departments."""
        response = client.get("/api/v1/departments/")
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
