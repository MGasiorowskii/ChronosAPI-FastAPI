from fastapi import APIRouter
from sqlmodel import select

from models import ConferenceRoom, User
from api.v1.deps import SessionDep, CurrentUser

router = APIRouter()


@router.get("/")
def read_rooms(session: SessionDep, user: CurrentUser):
    query = session.exec(
        select(ConferenceRoom)
        .join(ConferenceRoom.manager)
        .where(User.company_id == user.company_id)
    ).all()
    return query
