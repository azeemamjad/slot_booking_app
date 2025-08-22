from fastapi import APIRouter
from app.api.v1.routes import users, departments, games, slots, bookings, auth

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(departments.router)
api_router.include_router(games.router)
api_router.include_router(slots.router)
api_router.include_router(bookings.router)
