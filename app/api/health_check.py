import logging
from typing import Literal

from fastapi import APIRouter
from fastapi import status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlmodel import Session, select

from core.db import engine

router = APIRouter(prefix="/health", tags=["health-check"])


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HealthCheckStatus(BaseModel):
    status: Literal["ok", "nok"]

@router.get(
    "",
    summary="Perform a Health Check",
    response_description="Return HTTP Status Code 200 (OK) or 503 (Service Unavailable)",
)
def health_check():
    if _check_db() and _check_cache():
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=HealthCheckStatus(status='ok').model_dump(),
        )

    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content=HealthCheckStatus(status='nok').model_dump(),
    )


def _check_db() -> bool:
    try:
        with Session(engine) as session:
            session.exec(select(1))
            return True
    except Exception as e:
        logging.error(f"Database connection failed: {e}")
        return False

def _check_cache() -> bool:
    return True