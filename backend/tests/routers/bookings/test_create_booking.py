import pytest
from fastapi.testclient import TestClient
from fastapi import status
from datetime import datetime, timedelta


class TestCreateBooking:
    """Test cases for create booking endpoint."""
    
    def test_create_booking_user_success(self, client: TestClient, user_headers, admin_headers):
        """Test user can create booking for themselves."""
        # First create a game and slot as admin
        game_response = client.post(
            "/api/v1/games/",
            headers=admin_headers,
            json={
                "title": "Test Game for Booking",
                "description": "Test game for booking creation"
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
        
        # Get user ID from the user headers (assuming user is authenticated)
        # We'll need to get the user ID from the token or create a user first
        user_id = 1  # The user ID from the JWT token (user@test.com)
        
        response = client.post(
            "/api/v1/bookings/",
            headers=user_headers,
            json={
                "user_id": user_id,
                "slot_id": slot_id,
                "status": "CONFIRMED"
            }
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["user_id"] == user_id
        assert data["slot_id"] == slot_id
        assert data["status"] == "CONFIRMED"
        assert "id" in data
    
    def test_create_booking_admin_for_other_user(self, client: TestClient, admin_headers, normal_user):
        """Test admin can create booking for other users."""
        # First create a game and slot
        game_response = client.post(
            "/api/v1/games/",
            headers=admin_headers,
            json={
                "title": "Test Game for Admin Booking",
                "description": "Test game for admin booking"
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
        
        # Admin can create booking for any user
        response = client.post(
            "/api/v1/bookings/",
            headers=admin_headers,
            json={
                "user_id": 2,  # Different user (admin creating for user 2)
                "slot_id": slot_id,
                "status": "CONFIRMED"
            }
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["user_id"] == 2  # Admin created booking for user 2
        assert data["slot_id"] == slot_id
    
    def test_create_booking_user_for_other_user_forbidden(self, client: TestClient, user_headers, admin_headers):
        """Test user cannot create booking for other users."""
        # First create a game and slot as admin
        game_response = client.post(
            "/api/v1/games/",
            headers=admin_headers,
            json={
                "title": "Test Game for Forbidden Booking",
                "description": "Test game for forbidden booking"
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
        
        # User tries to create booking for different user
        response = client.post(
            "/api/v1/bookings/",
            headers=user_headers,
            json={
                "user_id": 999,  # Different user
                "slot_id": slot_id,
                "status": "CONFIRMED"
            }
        )
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_create_booking_unauthorized(self, client: TestClient, admin_headers):
        """Test unauthorized access to create booking."""
        # First create a game and slot as admin
        game_response = client.post(
            "/api/v1/games/",
            headers=admin_headers,
            json={
                "title": "Test Game for Unauthorized Booking",
                "description": "Test game for unauthorized booking"
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
        
        response = client.post(
            "/api/v1/bookings/",
            json={
                "user_id": 1,
                "slot_id": slot_id,
                "status": "CONFIRMED"
            }
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_create_booking_invalid_slot_id(self, client: TestClient, user_headers):
        """Test create booking with invalid slot ID."""
        response = client.post(
            "/api/v1/bookings/",
            headers=user_headers,
            json={
                "user_id": 1,
                "slot_id": 999,  # Non-existent slot
                "status": "CONFIRMED"
            }
        )
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_create_booking_slot_full(self, client: TestClient, user_headers, admin_headers):
        """Test create booking when slot is full."""
        # First create a game and slot with capacity 1
        game_response = client.post(
            "/api/v1/games/",
            headers=admin_headers,
            json={
                "title": "Test Game for Full Slot",
                "description": "Test game for full slot"
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
                "capacity": 1,  # Only 1 slot available
                "game_id": game_id
            }
        )
        slot_id = slot_response.json()["id"]
        
        # First booking should succeed
        response1 = client.post(
            "/api/v1/bookings/",
            headers=user_headers,
            json={
                "user_id": 1,
                "slot_id": slot_id,
                "status": "CONFIRMED"
            }
        )
        assert response1.status_code == status.HTTP_201_CREATED
        
        # Second booking should fail (slot is full)
        response2 = client.post(
            "/api/v1/bookings/",
            headers=user_headers,
            json={
                "user_id": 1,
                "slot_id": slot_id,
                "status": "CONFIRMED"
            }
        )
        
        assert response2.status_code == status.HTTP_400_BAD_REQUEST
        assert "full" in response2.json()["detail"].lower()
    
    def test_create_booking_missing_required_fields(self, client: TestClient, user_headers):
        """Test create booking with missing required fields."""
        response = client.post(
            "/api/v1/bookings/",
            headers=user_headers,
            json={
                "user_id": 1
                # Missing slot_id
            }
        )
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_create_booking_default_status(self, client: TestClient, user_headers, admin_headers):
        """Test create booking with default status."""
        # First create a game and slot as admin
        game_response = client.post(
            "/api/v1/games/",
            headers=admin_headers,
            json={
                "title": "Test Game for Default Status",
                "description": "Test game for default status"
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
        
        # Create booking without specifying status
        response = client.post(
            "/api/v1/bookings/",
            headers=user_headers,
            json={
                "user_id": 1,
                "slot_id": slot_id
                # No status specified, should use default
            }
        )
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["status"] == "CONFIRMED"  # Default status
