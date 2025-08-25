import pytest
from fastapi.testclient import TestClient
from fastapi import status


class TestGetGames:
    """Test cases for get games endpoints."""
    
    def test_get_games_success(self, client: TestClient, user_headers, admin_headers):
        """Test get all games."""
        # First create a game as admin
        create_response = client.post(
            "/api/v1/games/",
            headers=admin_headers,
            json={
                "title": "Test Game Get",
                "description": "Test description"
            }
        )
        
        response = client.get("/api/v1/games/", headers=user_headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1  # At least the game we just created
    
    def test_get_games_with_pagination(self, client: TestClient, user_headers, admin_headers):
        """Test get games with pagination."""
        # Create multiple games
        for i in range(3):
            client.post(
                "/api/v1/games/",
                headers=admin_headers,
                json={
                    "title": f"Test Game {i}",
                    "description": f"Test description {i}"
                }
            )
        
        response = client.get("/api/v1/games/?skip=0&limit=2", headers=user_headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) <= 2
    
    def test_get_games_unauthorized(self, client: TestClient):
        """Test unauthorized access to get games."""
        response = client.get("/api/v1/games/")
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_get_games_with_available_slots(self, client: TestClient, user_headers, admin_headers):
        """Test get games with available slots."""
        # First create a game as admin
        create_response = client.post(
            "/api/v1/games/",
            headers=admin_headers,
            json={
                "title": "Test Game Available",
                "description": "Test description"
            }
        )
        
        response = client.get("/api/v1/games/available/", headers=user_headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_games_with_available_slots_pagination(self, client: TestClient, user_headers, admin_headers):
        """Test get games with available slots and pagination."""
        # Create multiple games
        for i in range(3):
            client.post(
                "/api/v1/games/",
                headers=admin_headers,
                json={
                    "title": f"Test Game Available {i}",
                    "description": f"Test description {i}"
                }
            )
        
        response = client.get("/api/v1/games/available/?skip=0&limit=2", headers=user_headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) <= 2
    
    def test_get_games_with_available_slots_unauthorized(self, client: TestClient):
        """Test unauthorized access to get games with available slots."""
        response = client.get("/api/v1/games/available/")
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
