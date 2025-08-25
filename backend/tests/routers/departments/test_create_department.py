import pytest
from fastapi.testclient import TestClient
from fastapi import status


class TestCreateDepartment:
    """Test cases for create department endpoint."""
    
    def test_create_department_admin_success(self, client: TestClient, admin_headers):
        """Test admin can create department."""
        response = client.post(
            "/api/v1/departments/",
            headers=admin_headers,
            json={
                "title": "New Department Success",
                "description": "New department description"
            }
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["title"] == "New Department Success"
        assert data["description"] == "New department description"
        assert "id" in data
    
    def test_create_department_user_forbidden(self, client: TestClient, user_headers):
        """Test normal user cannot create departments."""
        response = client.post(
            "/api/v1/departments/",
            headers=user_headers,
            json={
                "title": "New Department Forbidden",
                "description": "New department description"
            }
        )
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_create_department_duplicate_title(self, client: TestClient, admin_headers):
        """Test create department with duplicate title."""
        # Create first department
        client.post(
            "/api/v1/departments/",
            headers=admin_headers,
            json={
                "title": "Duplicate Department Test",
                "description": "First department"
            }
        )
        
        # Try to create second with same title
        response = client.post(
            "/api/v1/departments/",
            headers=admin_headers,
            json={
                "title": "Duplicate Department Test",
                "description": "Second department"
            }
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "already exists" in response.json()["detail"]
    
    def test_create_department_unauthorized(self, client: TestClient):
        """Test unauthorized access to create department."""
        response = client.post(
            "/api/v1/departments/",
            json={
                "title": "New Department Unauthorized",
                "description": "New department description"
            }
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
