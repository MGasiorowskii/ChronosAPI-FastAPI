import secrets
from sqlmodel import select

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from fastapi import status, Request
from fastapi.responses import JSONResponse

from api.v1.deps import SessionDep, CurrentUser
from models import User
from core.db import cache


CACHE_TTL = 3600
router = APIRouter()


class CredentialsBody(BaseModel):
    email: str
    password: str


@router.post("/login")
async def login(session: SessionDep, credentials: CredentialsBody):
    user = session.exec(select(User).where(User.email == credentials.email)).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials"
        )
    elif not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    elif not user.verify_password(credentials.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid password"
        )

    session_id = secrets.token_hex(16)
    cache.set(session_id, str(user.id), ex=CACHE_TTL)
    response = JSONResponse(
        content={"message": "Logged in successfully"}
    )
    response.set_cookie(key="session_id", value=session_id)
    return response


@router.get("/logout")
async def logout(request: Request):
    session_id = request.cookies.get("session_id")
    if session_id is not None:
        cache.delete(session_id)

    response = JSONResponse(content={"message": "Logged out successfully"})
    response.delete_cookie("session_id")
    return response
