import pytest
from fastapi.testclient import TestClient
from fastapi import status
from datetime import datetime, timedelta


class TestGetBookings:
    """Test cases for get bookings endpoints."""
    
    def test_get_bookings_admin_success(self, client: TestClient, admin_headers, user_headers):
        """Test admin can get all bookings."""
        # First create a game, slot, and booking
        game_response = client.post(
            "/api/v1/games/",
            headers=admin_headers,
            json={
                "title": "Test Game for Get Bookings",
                "description": "Test game for getting bookings"
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
        client.post(
            "/api/v1/bookings/",
            headers=user_headers,
            json={
                "user_id": 2,
                "slot_id": slot_id,
                "status": "CONFIRMED"
            }
        )
        
        response = client.get("/api/v1/bookings/", headers=admin_headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1  # At least the booking we just created
    
    def test_get_bookings_user_forbidden(self, client: TestClient, user_headers):
        """Test normal user cannot get all bookings."""
        response = client.get("/api/v1/bookings/", headers=user_headers)
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_get_bookings_unauthorized(self, client: TestClient):
        """Test unauthorized access to get all bookings."""
        response = client.get("/api/v1/bookings/")
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_get_bookings_with_pagination(self, client: TestClient, admin_headers, user_headers):
        """Test get bookings with pagination."""
        # First create a game and slot
        game_response = client.post(
            "/api/v1/games/",
            headers=admin_headers,
            json={
                "title": "Test Game for Pagination",
                "description": "Test game for pagination"
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
        
        # Create multiple bookings
        for i in range(3):
            client.post(
                "/api/v1/bookings/",
                headers=user_headers,
                json={
                    "user_id": 1,
                    "slot_id": slot_id,
                    "status": "CONFIRMED"
                }
            )
        
        response = client.get("/api/v1/bookings/?skip=0&limit=2", headers=admin_headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) <= 2
    
    def test_get_bookings_by_user_success(self, client: TestClient, user_headers, admin_headers):
        """Test get bookings by user."""
        # First create a game, slot, and booking
        game_response = client.post(
            "/api/v1/games/",
            headers=admin_headers,
            json={
                "title": "Test Game for User Bookings",
                "description": "Test game for user bookings"
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
        
        # Create a booking for user 2
        client.post(
            "/api/v1/bookings/",
            headers=user_headers,
            json={
                "user_id": 1,
                "slot_id": slot_id,
                "status": "CONFIRMED"
            }
        )
        
        response = client.get("/api/v1/bookings/user/1", headers=user_headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
    
    def test_get_bookings_by_user_unauthorized(self, client: TestClient):
        """Test unauthorized access to get bookings by user."""
        response = client.get("/api/v1/bookings/user/2")
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_get_user_active_bookings(self, client: TestClient, user_headers, admin_headers):
        """Test get user active bookings."""
        # First create a game, slot, and booking
        game_response = client.post(
            "/api/v1/games/",
            headers=admin_headers,
            json={
                "title": "Test Game for Active Bookings",
                "description": "Test game for active bookings"
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
        
        # Create a confirmed booking
        client.post(
            "/api/v1/bookings/",
            headers=user_headers,
            json={
                "user_id": 1,
                "slot_id": slot_id,
                "status": "CONFIRMED"
            }
        )
        
        response = client.get("/api/v1/bookings/user/1/active", headers=user_headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        # Should only include confirmed bookings
    
    def test_get_bookings_by_slot(self, client: TestClient, user_headers, admin_headers):
        """Test get bookings by slot."""
        # First create a game, slot, and booking
        game_response = client.post(
            "/api/v1/games/",
            headers=admin_headers,
            json={
                "title": "Test Game for Slot Bookings",
                "description": "Test game for slot bookings"
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
        client.post(
            "/api/v1/bookings/",
            headers=user_headers,
            json={
                "user_id": 1,
                "slot_id": slot_id,
                "status": "CONFIRMED"
            }
        )
        
        response = client.get(f"/api/v1/bookings/slot/{slot_id}", headers=user_headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
    
    def test_get_bookings_by_status(self, client: TestClient, admin_headers, user_headers):
        """Test get bookings by status."""
        # First create a game, slot, and booking
        game_response = client.post(
            "/api/v1/games/",
            headers=admin_headers,
            json={
                "title": "Test Game for Status Bookings",
                "description": "Test game for status bookings"
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
        
        # Create a confirmed booking
        client.post(
            "/api/v1/bookings/",
            headers=user_headers,
            json={
                "user_id": 1,
                "slot_id": slot_id,
                "status": "CONFIRMED"
            }
        )
        
        response = client.get("/api/v1/bookings/status/CONFIRMED", headers=admin_headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        # Should only include confirmed bookings
    
    def test_get_bookings_by_status_unauthorized(self, client: TestClient):
        """Test unauthorized access to get bookings by status."""
        response = client.get("/api/v1/bookings/status/CONFIRMED")
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
