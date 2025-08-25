import pytest
from fastapi.testclient import TestClient
from fastapi import status


class TestCreateGame:
    """Test cases for create game endpoint."""
    
    def test_create_game_admin_success(self, client: TestClient, admin_headers):
        """Test admin can create game."""
        response = client.post(
            "/api/v1/games/",
            headers=admin_headers,
            json={
                "title": "New Game Success",
                "description": "New game description",
                "background": "game_background.jpg"
            }
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["title"] == "New Game Success"
        assert data["description"] == "New game description"
        assert data["background"] == "game_background.jpg"
        assert "id" in data
        assert "total_slots" in data
        assert "available_slots" in data
    
    def test_create_game_user_forbidden(self, client: TestClient, user_headers):
        """Test normal user cannot create games."""
        response = client.post(
            "/api/v1/games/",
            headers=user_headers,
            json={
                "title": "New Game Forbidden",
                "description": "New game description",
                "background": "game_background.jpg"
            }
        )
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_create_game_duplicate_title(self, client: TestClient, admin_headers):
        """Test create game with duplicate title."""
        # Create first game
        client.post(
            "/api/v1/games/",
            headers=admin_headers,
            json={
                "title": "Duplicate Game Test",
                "description": "First game"
            }
        )
        
        # Try to create second with same title
        response = client.post(
            "/api/v1/games/",
            headers=admin_headers,
            json={
                "title": "Duplicate Game Test",
                "description": "Second game"
            }
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "already exists" in response.json()["detail"]
    
    def test_create_game_unauthorized(self, client: TestClient):
        """Test unauthorized access to create game."""
        response = client.post(
            "/api/v1/games/",
            json={
                "title": "New Game Unauthorized",
                "description": "New game description"
            }
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_create_game_missing_required_fields(self, client: TestClient, admin_headers):
        """Test create game with missing required fields."""
        response = client.post(
            "/api/v1/games/",
            headers=admin_headers,
            json={
                "description": "Game description without title"
            }
        )
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_create_game_minimal_data(self, client: TestClient, admin_headers):
        """Test create game with minimal required data."""
        response = client.post(
            "/api/v1/games/",
            headers=admin_headers,
            json={
                "title": "Minimal Game"
            }
        )
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["title"] == "Minimal Game"
        assert data["description"] is None
        assert data["background"] is None
