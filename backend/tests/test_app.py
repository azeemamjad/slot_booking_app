from fastapi import FastAPI
from app.api.v1.api import api_router

# Create test app without startup events
test_app = FastAPI(title="Test API", version="1.0.0")
test_app.include_router(api_router, prefix="/api/v1")
