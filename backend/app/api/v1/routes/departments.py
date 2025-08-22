from fastapi import APIRouter

router = APIRouter(prefix="/departments", tags=["Departments"])

@router.get("/")
async def get_departments():
    return {"route": "GET /departments"}

@router.post("/")
async def create_department():
    return {"route": "POST /departments"}
