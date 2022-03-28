from fastapi import APIRouter

from app.api.routes import events

router = APIRouter()
router.include_router(events.router, tags=["events"], prefix="/events")
