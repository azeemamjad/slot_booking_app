from fastapi import APIRouter

router = APIRouter(prefix="/slots", tags=["Slots"])

@router.get("/")
async def get_slots():
    return {"route": "GET /slots"}

@router.post("/")
async def create_slot():
    return {"route": "POST /slots"}
