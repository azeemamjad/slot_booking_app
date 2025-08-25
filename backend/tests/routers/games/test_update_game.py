import pytest
from fastapi.testclient import TestClient
from fastapi import status


class TestUpdateGame:
    """Test cases for update game endpoint."""
    
    def test_update_game_admin_success(self, client: TestClient, admin_headers):
        """Test admin can update game."""
        # First create a game
        create_response = client.post(
            "/api/v1/games/",
            headers=admin_headers,
            json={
                "title": "Original Game",
                "description": "Original description"
            }
        )
        game_id = create_response.json()["id"]
        
        response = client.put(
            f"/api/v1/games/{game_id}",
            headers=admin_headers,
            json={
                "title": "Updated Game",
                "description": "Updated description",
                "background": "updated_background.jpg"
            }
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["title"] == "Updated Game"
        assert data["description"] == "Updated description"
        assert data["background"] == "updated_background.jpg"
    
    def test_update_game_user_forbidden(self, client: TestClient, user_headers, admin_headers):
        """Test normal user cannot update games."""
        # First create a game as admin
        create_response = client.post(
            "/api/v1/games/",
            headers=admin_headers,
            json={
                "title": "Test Game Update",
                "description": "Test description"
            }
        )
        game_id = create_response.json()["id"]
        
        response = client.put(
            f"/api/v1/games/{game_id}",
            headers=user_headers,
            json={
                "title": "Unauthorized Update"
            }
        )
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_update_game_not_found(self, client: TestClient, admin_headers):
        """Test update non-existent game."""
        response = client.put(
            "/api/v1/games/999",
            headers=admin_headers,
            json={
                "title": "Update"
            }
        )
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_update_game_unauthorized(self, client: TestClient):
        """Test unauthorized access to update game."""
        response = client.put(
            "/api/v1/games/1",
            json={
                "title": "Update"
            }
        )
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_update_game_partial(self, client: TestClient, admin_headers):
        """Test partial update of game."""
        # First create a game
        create_response = client.post(
            "/api/v1/games/",
            headers=admin_headers,
            json={
                "title": "Partial Update Game",
                "description": "Original description"
            }
        )
        game_id = create_response.json()["id"]
        
        response = client.put(
            f"/api/v1/games/{game_id}",
            headers=admin_headers,
            json={
                "title": "Updated Title Only"
            }
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["title"] == "Updated Title Only"
        assert data["description"] == "Original description"  # Should remain unchanged
    
    def test_update_game_duplicate_title(self, client: TestClient, admin_headers):
        """Test update game with duplicate title."""
        # Create first game
        client.post(
            "/api/v1/games/",
            headers=admin_headers,
            json={
                "title": "Duplicate Title Game",
                "description": "First game"
            }
        )
        
        # Create second game
        create_response = client.post(
            "/api/v1/games/",
            headers=admin_headers,
            json={
                "title": "Second Game",
                "description": "Second game"
            }
        )
        game_id = create_response.json()["id"]
        
        # Try to update second game with first game's title
        response = client.put(
            f"/api/v1/games/{game_id}",
            headers=admin_headers,
            json={
                "title": "Duplicate Title Game"
            }
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "already exists" in response.json()["detail"]
