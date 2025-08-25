import pytest
from fastapi.testclient import TestClient
from fastapi import status


class TestGetUsersByDepartment:
    """Test cases for get users by department endpoint."""
    
    def test_get_users_by_department_success(self, client: TestClient, user_headers, admin_headers):
        """Test get users by department."""
        # First create a department
        dept_response = client.post(
            "/api/v1/departments/",
            headers=admin_headers,
            json={
                "title": "Test Department Users",
                "description": "Test description"
            }
        )
        department_id = dept_response.json()["id"]
        
        response = client.get(
            f"/api/v1/users/department/{department_id}",
            headers=user_headers
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_users_by_department_with_pagination(self, client: TestClient, user_headers, admin_headers):
        """Test get users by department with pagination."""
        # First create a department
        dept_response = client.post(
            "/api/v1/departments/",
            headers=admin_headers,
            json={
                "title": "Test Department 2",
                "description": "Test description"
            }
        )
        department_id = dept_response.json()["id"]
        
        response = client.get(
            f"/api/v1/users/department/{department_id}?skip=0&limit=10",
            headers=user_headers
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) <= 10
    
    def test_get_users_by_department_not_found(self, client: TestClient, user_headers):
        """Test get users by non-existent department."""
        response = client.get(
            "/api/v1/users/department/999",
            headers=user_headers
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0  # Empty list for non-existent department
    
    def test_get_users_by_department_unauthorized(self, client: TestClient):
        """Test unauthorized access to get users by department."""
        response = client.get("/api/v1/users/department/1")
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
