import pytest
from fastapi.testclient import TestClient
from fastapi import status
from datetime import datetime, timedelta


class TestGetSlots:
    """Test cases for get slots endpoints."""
    
    def test_get_slots_success(self, client: TestClient, user_headers, admin_headers):
        """Test get all slots."""
        # First create a game and slot as admin
        game_response = client.post(
            "/api/v1/games/",
            headers=admin_headers,
            json={
                "title": "Test Game for Get Slots",
                "description": "Test game for getting slots"
            }
        )
        game_id = game_response.json()["id"]
        
        start_time = datetime.now() + timedelta(hours=1)
        end_time = start_time + timedelta(hours=2)
        
        client.post(
            "/api/v1/slots/",
            headers=admin_headers,
            json={
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "capacity": 4,
                "game_id": game_id
            }
        )
        
        response = client.get("/api/v1/slots/", headers=user_headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1  # At least the slot we just created
    
    def test_get_slots_with_pagination(self, client: TestClient, user_headers, admin_headers):
        """Test get slots with pagination."""
        # First create a game as admin
        game_response = client.post(
            "/api/v1/games/",
            headers=admin_headers,
            json={
                "title": "Test Game for Pagination",
                "description": "Test game for pagination"
            }
        )
        game_id = game_response.json()["id"]
        
        # Create multiple slots
        for i in range(3):
            start_time = datetime.now() + timedelta(hours=i+1)
            end_time = start_time + timedelta(hours=2)
            
            client.post(
                "/api/v1/slots/",
                headers=admin_headers,
                json={
                    "start_time": start_time.isoformat(),
                    "end_time": end_time.isoformat(),
                    "capacity": 4,
                    "game_id": game_id
                }
            )
        
        response = client.get("/api/v1/slots/?skip=0&limit=2", headers=user_headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) <= 2
    
    def test_get_slots_unauthorized(self, client: TestClient):
        """Test unauthorized access to get slots."""
        response = client.get("/api/v1/slots/")
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_get_available_slots(self, client: TestClient, user_headers, admin_headers):
        """Test get available slots."""
        # First create a game and slot as admin
        game_response = client.post(
            "/api/v1/games/",
            headers=admin_headers,
            json={
                "title": "Test Game for Available Slots",
                "description": "Test game for available slots"
            }
        )
        game_id = game_response.json()["id"]
        
        start_time = datetime.now() + timedelta(hours=1)
        end_time = start_time + timedelta(hours=2)
        
        client.post(
            "/api/v1/slots/",
            headers=admin_headers,
            json={
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "capacity": 4,
                "game_id": game_id
            }
        )
        
        response = client.get("/api/v1/slots/available/", headers=user_headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_available_slots_pagination(self, client: TestClient, user_headers, admin_headers):
        """Test get available slots with pagination."""
        # First create a game as admin
        game_response = client.post(
            "/api/v1/games/",
            headers=admin_headers,
            json={
                "title": "Test Game for Available Pagination",
                "description": "Test game for available pagination"
            }
        )
        game_id = game_response.json()["id"]
        
        # Create multiple slots
        for i in range(3):
            start_time = datetime.now() + timedelta(hours=i+1)
            end_time = start_time + timedelta(hours=2)
            
            client.post(
                "/api/v1/slots/",
                headers=admin_headers,
                json={
                    "start_time": start_time.isoformat(),
                    "end_time": end_time.isoformat(),
                    "capacity": 4,
                    "game_id": game_id
                }
            )
        
        response = client.get("/api/v1/slots/available/?skip=0&limit=2", headers=user_headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) <= 2
    
    def test_get_available_slots_unauthorized(self, client: TestClient):
        """Test unauthorized access to get available slots."""
        response = client.get("/api/v1/slots/available/")
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_get_slots_by_game(self, client: TestClient, user_headers, admin_headers):
        """Test get slots by game."""
        # First create a game and slot as admin
        game_response = client.post(
            "/api/v1/games/",
            headers=admin_headers,
            json={
                "title": "Test Game for Slots by Game",
                "description": "Test game for slots by game"
            }
        )
        game_id = game_response.json()["id"]
        
        start_time = datetime.now() + timedelta(hours=1)
        end_time = start_time + timedelta(hours=2)
        
        client.post(
            "/api/v1/slots/",
            headers=admin_headers,
            json={
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "capacity": 4,
                "game_id": game_id
            }
        )
        
        response = client.get(f"/api/v1/slots/game/{game_id}", headers=user_headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
    
    def test_get_slots_by_game_not_found(self, client: TestClient, user_headers):
        """Test get slots by non-existent game."""
        response = client.get("/api/v1/slots/game/999", headers=user_headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0  # Empty list for non-existent game
    
    def test_get_slots_by_date_range(self, client: TestClient, user_headers, admin_headers):
        """Test get slots by date range."""
        # First create a game and slot as admin
        game_response = client.post(
            "/api/v1/games/",
            headers=admin_headers,
            json={
                "title": "Test Game for Date Range",
                "description": "Test game for date range"
            }
        )
        game_id = game_response.json()["id"]
        
        start_time = datetime.now() + timedelta(hours=1)
        end_time = start_time + timedelta(hours=2)
        
        client.post(
            "/api/v1/slots/",
            headers=admin_headers,
            json={
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "capacity": 4,
                "game_id": game_id
            }
        )
        
        # Query for slots in the next 24 hours
        query_start = datetime.now()
        query_end = datetime.now() + timedelta(hours=24)
        
        response = client.get(
            f"/api/v1/slots/date-range/?start_date={query_start.isoformat()}&end_date={query_end.isoformat()}",
            headers=user_headers
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
    
    def test_get_slots_by_date_range_unauthorized(self, client: TestClient):
        """Test unauthorized access to get slots by date range."""
        query_start = datetime.now()
        query_end = datetime.now() + timedelta(hours=24)
        
        response = client.get(
            f"/api/v1/slots/date-range/?start_date={query_start.isoformat()}&end_date={query_end.isoformat()}"
        )
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
