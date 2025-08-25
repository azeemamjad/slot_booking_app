import pytest
from fastapi.testclient import TestClient
from fastapi import status
from datetime import datetime, timedelta


class TestGetBooking:
    """Test cases for get specific booking endpoint."""
    
    def test_get_booking_owner_success(self, client: TestClient, user_headers, admin_headers):
        """Test user can get their own booking."""
        # First create a game, slot, and booking
        game_response = client.post(
            "/api/v1/games/",
            headers=admin_headers,
            json={
                "title": "Test Game for Get Booking",
                "description": "Test game for getting booking"
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
        
        # Create a booking
        create_response = client.post(
            "/api/v1/bookings/",
            headers=user_headers,
            json={
                "user_id": 1,
                "slot_id": slot_id,
                "status": "CONFIRMED"
            }
        )
        booking_id = create_response.json()["id"]
        
        response = client.get(f"/api/v1/bookings/{booking_id}", headers=user_headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == booking_id
        assert data["user_id"] == 1
        assert data["slot_id"] == slot_id
        assert data["status"] == "CONFIRMED"
    
    def test_get_booking_admin_success(self, client: TestClient, user_headers, admin_headers):
        """Test admin can get any booking."""
        # First create a game, slot, and booking
        game_response = client.post(
            "/api/v1/games/",
            headers=admin_headers,
            json={
                "title": "Test Game for Admin Get Booking",
                "description": "Test game for admin getting booking"
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
        
        # Create a booking
        create_response = client.post(
            "/api/v1/bookings/",
            headers=user_headers,
            json={
                "user_id": 1,
                "slot_id": slot_id,
                "status": "CONFIRMED"
            }
        )
        booking_id = create_response.json()["id"]
        
        response = client.get(f"/api/v1/bookings/{booking_id}", headers=admin_headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == booking_id
    
    def test_get_booking_not_owner_forbidden(self, client: TestClient, user_headers, admin_headers, normal_user):
        """Test user cannot get booking they don't own."""
        # First create a game, slot, and booking as admin
        game_response = client.post(
            "/api/v1/games/",
            headers=admin_headers,
            json={
                "title": "Test Game for Forbidden Get Booking",
                "description": "Test game for forbidden getting booking"
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
        
        # Create a booking for user 2 (normal user)
        create_response = client.post(
            "/api/v1/bookings/",
            headers=admin_headers,
            json={
                "user_id": 2,
                "slot_id": slot_id,
                "status": "CONFIRMED"
            }
        )
        booking_id = create_response.json()["id"]
        
        # User 1 tries to get booking owned by user 2
        response = client.get(f"/api/v1/bookings/{booking_id}", headers=user_headers)
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_get_booking_not_found(self, client: TestClient, user_headers):
        """Test get non-existent booking."""
        response = client.get("/api/v1/bookings/999", headers=user_headers)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_get_booking_unauthorized(self, client: TestClient):
        """Test unauthorized access to get booking."""
        response = client.get("/api/v1/bookings/1")
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_get_booking_invalid_id(self, client: TestClient, user_headers):
        """Test get booking with invalid ID."""
        response = client.get("/api/v1/bookings/invalid", headers=user_headers)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
