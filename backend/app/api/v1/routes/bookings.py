from fastapi import APIRouter

router = APIRouter(prefix="/bookings", tags=["Bookings"])

@router.get("/")
async def get_bookings():
    return {"route": "GET /bookings"}

@router.post("/")
async def create_booking():
    return {"route": "POST /bookings"}
