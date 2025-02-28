from fastapi import APIRouter
from app.api.v1.views import auth
from core.config import settings

router = APIRouter(prefix=settings.API_V1_STR)
router.include_router(auth.router, prefix="/auth", tags=["auth"])
