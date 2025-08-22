from fastapi import APIRouter

router = APIRouter(prefix="/games", tags=["Games"])

@router.get("/")
async def get_games():
    return {"route": "GET /games"}

@router.post("/")
async def create_game():
    return {"route": "POST /games"}
