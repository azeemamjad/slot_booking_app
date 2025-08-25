import pytest
from fastapi.testclient import TestClient
from fastapi import status
from datetime import datetime, timedelta


class TestCreateSlot:
    """Test cases for create slot endpoint."""
    
    def test_create_slot_admin_success(self, client: TestClient, admin_headers):
        """Test admin can create slot."""
        # First create a game
        game_response = client.post(
            "/api/v1/games/",
            headers=admin_headers,
            json={
                "title": "Test Game for Slot",
                "description": "Test game for slot creation"
            }
        )
        game_id = game_response.json()["id"]
        
        start_time = datetime.now() + timedelta(hours=1)
        end_time = start_time + timedelta(hours=2)
        
        response = client.post(
            "/api/v1/slots/",
            headers=admin_headers,
            json={
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "capacity": 4,
                "game_id": game_id
            }
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["capacity"] == 4
        assert data["game_id"] == game_id
        assert "id" in data
        assert "slots_booked_count" in data
        assert "is_full" in data
    
    def test_create_slot_user_forbidden(self, client: TestClient, user_headers, admin_headers):
        """Test normal user cannot create slots."""
        # First create a game as admin
        game_response = client.post(
            "/api/v1/games/",
            headers=admin_headers,
            json={
                "title": "Test Game for Slot Forbidden",
                "description": "Test game for slot creation"
            }
        )
        game_id = game_response.json()["id"]
        
        start_time = datetime.now() + timedelta(hours=1)
        end_time = start_time + timedelta(hours=2)
        
        response = client.post(
            "/api/v1/slots/",
            headers=user_headers,
            json={
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "capacity": 4,
                "game_id": game_id
            }
        )
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_create_slot_unauthorized(self, client: TestClient, admin_headers):
        """Test unauthorized access to create slot."""
        # First create a game
        game_response = client.post(
            "/api/v1/games/",
            headers=admin_headers,
            json={
                "title": "Test Game for Slot Unauthorized",
                "description": "Test game for slot creation"
            }
        )
        game_id = game_response.json()["id"]
        
        start_time = datetime.now() + timedelta(hours=1)
        end_time = start_time + timedelta(hours=2)
        
        response = client.post(
            "/api/v1/slots/",
            json={
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "capacity": 4,
                "game_id": game_id
            }
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_create_slot_missing_required_fields(self, client: TestClient, admin_headers):
        """Test create slot with missing required fields."""
        response = client.post(
            "/api/v1/slots/",
            headers=admin_headers,
            json={
                "start_time": datetime.now().isoformat()
                # Missing end_time and game_id
            }
        )
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_create_slot_invalid_game_id(self, client: TestClient, admin_headers):
        """Test create slot with invalid game ID."""
        start_time = datetime.now() + timedelta(hours=1)
        end_time = start_time + timedelta(hours=2)
        
        response = client.post(
            "/api/v1/slots/",
            headers=admin_headers,
            json={
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "capacity": 4,
                "game_id": 999  # Non-existent game
            }
        )
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_create_slot_invalid_time_range(self, client: TestClient, admin_headers):
        """Test create slot with end_time before start_time."""
        # First create a game
        game_response = client.post(
            "/api/v1/games/",
            headers=admin_headers,
            json={
                "title": "Test Game for Invalid Time",
                "description": "Test game for invalid time slot"
            }
        )
        game_id = game_response.json()["id"]
        
        start_time = datetime.now() + timedelta(hours=2)
        end_time = start_time - timedelta(hours=1)  # End before start
        
        response = client.post(
            "/api/v1/slots/",
            headers=admin_headers,
            json={
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "capacity": 4,
                "game_id": game_id
            }
        )
        
        # This should fail validation (could be 400 or 422 depending on implementation)
        assert response.status_code in [status.HTTP_400_BAD_REQUEST, status.HTTP_422_UNPROCESSABLE_ENTITY]
    
    def test_create_slot_default_capacity(self, client: TestClient, admin_headers):
        """Test create slot with default capacity."""
        # First create a game
        game_response = client.post(
            "/api/v1/games/",
            headers=admin_headers,
            json={
                "title": "Test Game for Default Capacity",
                "description": "Test game for default capacity"
            }
        )
        game_id = game_response.json()["id"]
        
        start_time = datetime.now() + timedelta(hours=1)
        end_time = start_time + timedelta(hours=2)
        
        response = client.post(
            "/api/v1/slots/",
            headers=admin_headers,
            json={
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "game_id": game_id
                # No capacity specified, should use default
            }
        )
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["capacity"] == 2  # Default capacity
