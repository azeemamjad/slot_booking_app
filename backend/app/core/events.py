from fastapi import FastAPI
from app.db.session import AsyncSessionLocal
from app.db.init_db import init_db

def init_app_events(app: FastAPI):
    @app.on_event("startup")
    async def on_startup():
        async with AsyncSessionLocal() as db:
            await init_db(db)   # make sure init_db is async

    @app.on_event("shutdown")
    async def on_shutdown():
        print("Application shutdown complete.")
