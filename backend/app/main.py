from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.core.config import settings
from app.core.events import init_app_events
from app.api.v1.api import api_router
from app.db.session import get_db

app = FastAPI(title=settings.PROJECT_NAME)

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