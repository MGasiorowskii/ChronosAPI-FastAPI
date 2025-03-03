from fastapi import APIRouter
from app.api.v1.views import auth, rooms, events
from core.config import settings

router = APIRouter(prefix=settings.API_V1_STR)
router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(rooms.router, prefix="/rooms", tags=["rooms"])
router.include_router(events.router, prefix="/events", tags=["events"])
