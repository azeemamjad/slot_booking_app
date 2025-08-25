import pytest
from fastapi.testclient import TestClient
from fastapi import status


class TestGetGame:
    """Test cases for get specific game endpoint."""
    
    def test_get_game_success(self, client: TestClient, user_headers, admin_headers):
        """Test get specific game."""
        # First create a game as admin
        create_response = client.post(
            "/api/v1/games/",
            headers=admin_headers,
            json={
                "title": "Test Game Get Specific",
                "description": "Test description"
            }
        )
        game_id = create_response.json()["id"]
        
        response = client.get(f"/api/v1/games/{game_id}", headers=user_headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == game_id
        assert data["title"] == "Test Game Get Specific"
        assert data["description"] == "Test description"
    
    def test_get_game_not_found(self, client: TestClient, user_headers):
        """Test get non-existent game."""
        response = client.get("/api/v1/games/999", headers=user_headers)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_get_game_unauthorized(self, client: TestClient):
        """Test unauthorized access to get game."""
        response = client.get("/api/v1/games/1")
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_get_game_invalid_id(self, client: TestClient, user_headers):
        """Test get game with invalid ID."""
        response = client.get("/api/v1/games/invalid", headers=user_headers)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
