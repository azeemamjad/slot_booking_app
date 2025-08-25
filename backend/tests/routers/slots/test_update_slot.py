import pytest
from fastapi.testclient import TestClient
from fastapi import status
from datetime import datetime, timedelta


class TestUpdateSlot:
    """Test cases for update slot endpoint."""
    
    def test_update_slot_admin_success(self, client: TestClient, admin_headers):
        """Test admin can update slot."""
        # First create a game and slot
        game_response = client.post(
            "/api/v1/games/",
            headers=admin_headers,
            json={
                "title": "Test Game for Update Slot",
                "description": "Test game for updating slot"
            }
        )
        game_id = game_response.json()["id"]
        
        start_time = datetime.now() + timedelta(hours=1)
        end_time = start_time + timedelta(hours=2)
        
        create_response = client.post(
            "/api/v1/slots/",
            headers=admin_headers,
            json={
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "capacity": 4,
                "game_id": game_id
            }
        )
        slot_id = create_response.json()["id"]
        
        # Update the slot
        new_start_time = datetime.now() + timedelta(hours=2)
        new_end_time = new_start_time + timedelta(hours=3)
        
        response = client.put(
            f"/api/v1/slots/{slot_id}",
            headers=admin_headers,
            json={
                "capacity": 6,
                "start_time": new_start_time.isoformat(),
                "end_time": new_end_time.isoformat()
            }
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["capacity"] == 6
        assert data["game_id"] == game_id
    
    def test_update_slot_user_forbidden(self, client: TestClient, user_headers, admin_headers):
        """Test normal user cannot update slots."""
        # First create a game and slot as admin
        game_response = client.post(
            "/api/v1/games/",
            headers=admin_headers,
            json={
                "title": "Test Game for Update Forbidden",
                "description": "Test game for update forbidden"
            }
        )
        game_id = game_response.json()["id"]
        
        start_time = datetime.now() + timedelta(hours=1)
        end_time = start_time + timedelta(hours=2)
        
        create_response = client.post(
            "/api/v1/slots/",
            headers=admin_headers,
            json={
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "capacity": 4,
                "game_id": game_id
            }
        )
        slot_id = create_response.json()["id"]
        
        response = client.put(
            f"/api/v1/slots/{slot_id}",
            headers=user_headers,
            json={
                "capacity": 6
            }
        )
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_update_slot_not_found(self, client: TestClient, admin_headers):
        """Test update non-existent slot."""
        response = client.put(
            "/api/v1/slots/999",
            headers=admin_headers,
            json={
                "capacity": 6
            }
        )
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_update_slot_unauthorized(self, client: TestClient):
        """Test unauthorized access to update slot."""
        response = client.put(
            "/api/v1/slots/1",
            json={
                "capacity": 6
            }
        )
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_update_slot_partial(self, client: TestClient, admin_headers):
        """Test partial update of slot."""
        # First create a game and slot
        game_response = client.post(
            "/api/v1/games/",
            headers=admin_headers,
            json={
                "title": "Test Game for Partial Update",
                "description": "Test game for partial update"
            }
        )
        game_id = game_response.json()["id"]
        
        start_time = datetime.now() + timedelta(hours=1)
        end_time = start_time + timedelta(hours=2)
        
        create_response = client.post(
            "/api/v1/slots/",
            headers=admin_headers,
            json={
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "capacity": 4,
                "game_id": game_id
            }
        )
        slot_id = create_response.json()["id"]
        
        # Update only capacity
        response = client.put(
            f"/api/v1/slots/{slot_id}",
            headers=admin_headers,
            json={
                "capacity": 8
            }
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["capacity"] == 8
        assert data["game_id"] == game_id  # Should remain unchanged
    
    def test_update_slot_invalid_game_id(self, client: TestClient, admin_headers):
        """Test update slot with invalid game ID."""
        # First create a game and slot
        game_response = client.post(
            "/api/v1/games/",
            headers=admin_headers,
            json={
                "title": "Test Game for Invalid Game Update",
                "description": "Test game for invalid game update"
            }
        )
        game_id = game_response.json()["id"]
        
        start_time = datetime.now() + timedelta(hours=1)
        end_time = start_time + timedelta(hours=2)
        
        create_response = client.post(
            "/api/v1/slots/",
            headers=admin_headers,
            json={
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "capacity": 4,
                "game_id": game_id
            }
        )
        slot_id = create_response.json()["id"]
        
        # Try to update with non-existent game
        response = client.put(
            f"/api/v1/slots/{slot_id}",
            headers=admin_headers,
            json={
                "game_id": 999
            }
        )
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
