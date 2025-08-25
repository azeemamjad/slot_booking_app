import pytest
import asyncio
from tests.conftest import client, admin_user

async def debug_login():
    """Debug login issue."""
    async for test_client in client():
        response = test_client.post(
            "/api/v1/auth/login",
            json={
                "username": "admin@test.com",
                "password": "admin123"
            }
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        break

if __name__ == "__main__":
    asyncio.run(debug_login())
