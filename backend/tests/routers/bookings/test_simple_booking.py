import pytest
from fastapi.testclient import TestClient
from fastapi import status
from datetime import datetime, timedelta


class TestSimpleBooking:
    """Simple test cases for booking functionality."""
    
    def test_create_booking_simple(self, client: TestClient, admin_headers, user_headers):
        """Test simple booking creation."""
        # First create a game and slot as admin
        game_response = client.post(
            "/api/v1/games/",
            headers=admin_headers,
            json={
                "title": "Simple Test Game",
                "description": "Simple test game"
            }
        )
        game_id = game_response.json()["id"]
        
        start_time = datetime.now() + timedelta(hours=1)
        end_time = start_time + timedelta(hours=2)
        
        slot_response = client.post(
            "/api/v1/slots/",
            headers=admin_headers,
            json={
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "capacity": 4,
                "game_id": game_id
            }
        )
        slot_id = slot_response.json()["id"]
        
        # Create a booking as admin for user 2
        response = client.post(
            "/api/v1/bookings/",
            headers=admin_headers,
            json={
                "user_id": 2,
                "slot_id": slot_id,
                "status": "CONFIRMED"
            }
        )
        
        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.text}")
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["user_id"] == 2
        assert data["slot_id"] == slot_id
        assert data["status"] == "CONFIRMED"
