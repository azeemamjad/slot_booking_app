from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.core.config import settings
from app.core.events import init_app_events
from app.api.v1.api import api_router
from app.db.session import get_db

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_tags=[
        {"name": "Authentication", "description": "Authentication operations"},
        {"name": "Users", "description": "User management operations"},
        {"name": "Departments", "description": "Department management operations"},
        {"name": "Games", "description": "Game management operations"},
        {"name": "Slots", "description": "Slot management operations"},
        {"name": "Bookings", "description": "Booking management operations"},
    ]
)

# Configure CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React default
        "http://localhost:8080",  # Vue default
        "http://localhost:4200",  # Angular default
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8080",
        "http://127.0.0.1:4200",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_app_events(app)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root(db: AsyncSession = Depends(get_db)):
    try:
        # Run a simple query to test DB connection
        await db.execute(text("SELECT 1"))
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"

    return {
        "message": "Slot Booking App API is running",
        "database": db_status,
    }