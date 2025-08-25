import pytest
from fastapi.testclient import TestClient
from fastapi import status
from datetime import datetime, timedelta


class TestBookingOperations:
    """Test cases for booking operations (update, cancel, confirm, delete)."""
    
    def test_update_booking_owner_success(self, client: TestClient, user_headers, admin_headers):
        """Test user can update their own booking."""
        # First create a game, slot, and booking
        game_response = client.post(
            "/api/v1/games/",
            headers=admin_headers,
            json={
                "title": "Test Game for Update Booking",
                "description": "Test game for updating booking"
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
                "status": "PENDING"
            }
        )
        booking_id = create_response.json()["id"]
        
        # Update the booking
        response = client.put(
            f"/api/v1/bookings/{booking_id}",
            headers=user_headers,
            json={
                "status": "CONFIRMED"
            }
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "CONFIRMED"
    
    def test_update_booking_admin_success(self, client: TestClient, user_headers, admin_headers):
        """Test admin can update any booking."""
        # First create a game, slot, and booking
        game_response = client.post(
            "/api/v1/games/",
            headers=admin_headers,
            json={
                "title": "Test Game for Admin Update Booking",
                "description": "Test game for admin updating booking"
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
                "status": "PENDING"
            }
        )
        booking_id = create_response.json()["id"]
        
        # Admin updates the booking
        response = client.put(
            f"/api/v1/bookings/{booking_id}",
            headers=admin_headers,
            json={
                "status": "CONFIRMED"
            }
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "CONFIRMED"
    
    def test_update_booking_not_owner_forbidden(self, client: TestClient, user_headers, admin_headers, normal_user):
        """Test user cannot update booking they don't own."""
        # First create a game, slot, and booking as admin
        game_response = client.post(
            "/api/v1/games/",
            headers=admin_headers,
            json={
                "title": "Test Game for Forbidden Update Booking",
                "description": "Test game for forbidden updating booking"
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
                "status": "PENDING"
            }
        )
        booking_id = create_response.json()["id"]
        
        # User 1 tries to update booking owned by user 2
        response = client.put(
            f"/api/v1/bookings/{booking_id}",
            headers=user_headers,
            json={
                "status": "CONFIRMED"
            }
        )
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_cancel_booking_owner_success(self, client: TestClient, user_headers, admin_headers):
        """Test user can cancel their own booking."""
        # First create a game, slot, and booking
        game_response = client.post(
            "/api/v1/games/",
            headers=admin_headers,
            json={
                "title": "Test Game for Cancel Booking",
                "description": "Test game for canceling booking"
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
        
        # Cancel the booking
        response = client.post(
            f"/api/v1/bookings/{booking_id}/cancel",
            headers=user_headers
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "CANCELLED"
    
    def test_cancel_booking_admin_success(self, client: TestClient, user_headers, admin_headers):
        """Test admin can cancel any booking."""
        # First create a game, slot, and booking
        game_response = client.post(
            "/api/v1/games/",
            headers=admin_headers,
            json={
                "title": "Test Game for Admin Cancel Booking",
                "description": "Test game for admin canceling booking"
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
        
        # Admin cancels the booking
        response = client.post(
            f"/api/v1/bookings/{booking_id}/cancel",
            headers=admin_headers
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "CANCELLED"
    
    def test_confirm_booking_admin_success(self, client: TestClient, user_headers, admin_headers):
        """Test admin can confirm a pending booking."""
        # First create a game, slot, and booking
        game_response = client.post(
            "/api/v1/games/",
            headers=admin_headers,
            json={
                "title": "Test Game for Confirm Booking",
                "description": "Test game for confirming booking"
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
        
        # Create a pending booking
        create_response = client.post(
            "/api/v1/bookings/",
            headers=user_headers,
            json={
                "user_id": 1,
                "slot_id": slot_id,
                "status": "PENDING"
            }
        )
        booking_id = create_response.json()["id"]
        
        # Admin confirms the booking
        response = client.post(
            f"/api/v1/bookings/{booking_id}/confirm",
            headers=admin_headers
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "CONFIRMED"
    
    def test_confirm_booking_user_forbidden(self, client: TestClient, user_headers, admin_headers):
        """Test user cannot confirm bookings."""
        # First create a game, slot, and booking
        game_response = client.post(
            "/api/v1/games/",
            headers=admin_headers,
            json={
                "title": "Test Game for Forbidden Confirm Booking",
                "description": "Test game for forbidden confirming booking"
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
        
        # Create a pending booking
        create_response = client.post(
            "/api/v1/bookings/",
            headers=user_headers,
            json={
                "user_id": 1,
                "slot_id": slot_id,
                "status": "PENDING"
            }
        )
        booking_id = create_response.json()["id"]
        
        # User tries to confirm the booking
        response = client.post(
            f"/api/v1/bookings/{booking_id}/confirm",
            headers=user_headers
        )
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_delete_booking_admin_success(self, client: TestClient, user_headers, admin_headers):
        """Test admin can delete any booking."""
        # First create a game, slot, and booking
        game_response = client.post(
            "/api/v1/games/",
            headers=admin_headers,
            json={
                "title": "Test Game for Delete Booking",
                "description": "Test game for deleting booking"
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
        
        # Admin deletes the booking
        response = client.delete(
            f"/api/v1/bookings/{booking_id}",
            headers=admin_headers
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "message" in data
        assert "deleted successfully" in data["message"]
    
    def test_delete_booking_user_forbidden(self, client: TestClient, user_headers, admin_headers):
        """Test user cannot delete bookings."""
        # First create a game, slot, and booking
        game_response = client.post(
            "/api/v1/games/",
            headers=admin_headers,
            json={
                "title": "Test Game for Forbidden Delete Booking",
                "description": "Test game for forbidden deleting booking"
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
        
        # User tries to delete the booking
        response = client.delete(
            f"/api/v1/bookings/{booking_id}",
            headers=user_headers
        )
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_reset_current_day_bookings_admin_success(self, client: TestClient, admin_headers):
        """Test admin can reset current day bookings."""
        response = client.post(
            "/api/v1/bookings/reset-current-day",
            headers=admin_headers
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "message" in data
    
    def test_reset_current_day_bookings_user_forbidden(self, client: TestClient, user_headers):
        """Test user cannot reset current day bookings."""
        response = client.post(
            "/api/v1/bookings/reset-current-day",
            headers=user_headers
        )
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_booking_not_found_operations(self, client: TestClient, admin_headers):
        """Test operations on non-existent booking."""
        # Test update
        response = client.put(
            "/api/v1/bookings/999",
            headers=admin_headers,
            json={
                "status": "CONFIRMED"
            }
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
        
        # Test cancel
        response = client.post(
            "/api/v1/bookings/999/cancel",
            headers=admin_headers
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
        
        # Test confirm
        response = client.post(
            "/api/v1/bookings/999/confirm",
            headers=admin_headers
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
        
        # Test delete
        response = client.delete(
            "/api/v1/bookings/999",
            headers=admin_headers
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
