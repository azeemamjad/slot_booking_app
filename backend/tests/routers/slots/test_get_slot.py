import pytest
from fastapi.testclient import TestClient
from fastapi import status
from datetime import datetime, timedelta


class TestGetSlot:
    """Test cases for get specific slot endpoint."""
    
    def test_get_slot_success(self, client: TestClient, user_headers, admin_headers):
        """Test get specific slot."""
        # First create a game and slot as admin
        game_response = client.post(
            "/api/v1/games/",
            headers=admin_headers,
            json={
                "title": "Test Game for Get Slot",
                "description": "Test game for getting slot"
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
        
        response = client.get(f"/api/v1/slots/{slot_id}", headers=user_headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == slot_id
        assert data["capacity"] == 4
        assert data["game_id"] == game_id
        assert "slots_booked_count" in data
        assert "is_full" in data
    
    def test_get_slot_not_found(self, client: TestClient, user_headers):
        """Test get non-existent slot."""
        response = client.get("/api/v1/slots/999", headers=user_headers)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_get_slot_unauthorized(self, client: TestClient):
        """Test unauthorized access to get slot."""
        response = client.get("/api/v1/slots/1")
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_get_slot_invalid_id(self, client: TestClient, user_headers):
        """Test get slot with invalid ID."""
        response = client.get("/api/v1/slots/invalid", headers=user_headers)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
