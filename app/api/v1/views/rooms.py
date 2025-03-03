from fastapi import APIRouter, HTTPException
from sqlmodel import select

from models import ConferenceRoom, User, ResponseConferenceRoom, CreateConferenceRoom
from api.v1.deps import SessionDep, CurrentUser

router = APIRouter()


@router.get("/", response_model=list[ResponseConferenceRoom])
def read_rooms(session: SessionDep, user: CurrentUser):
    query = session.exec(
        select(ConferenceRoom)
        .join(ConferenceRoom.manager)
        .where(User.company_id == user.company_id)
    ).all()
    return [ResponseConferenceRoom.from_orm(room) for room in query]


@router.get("/{room_id}", response_model=ResponseConferenceRoom)
def read_room(room_id: int, session: SessionDep, user: CurrentUser):
    query = session.exec(
        select(ConferenceRoom)
        .join(ConferenceRoom.manager)
        .where(User.company_id == user.company_id)
        .where(ConferenceRoom.id == room_id)
    ).one_or_none()
    return ResponseConferenceRoom.from_orm(query) if query else []


@router.post("/", response_model=ResponseConferenceRoom)
def create_room(data: CreateConferenceRoom, session: SessionDep, user: CurrentUser):
    manager = session.exec(
        select(User).where(
            User.email == data.manager, User.company_id == user.company_id
        )
    ).one_or_none()
    if not manager:
        raise HTTPException(status_code=400, detail="Manager not found")

    room = ConferenceRoom(
        name=data.name,
        address=data.address,
        manager_id=manager.id,
    )
    session.add(room)
    session.commit()
    session.refresh(room)
    return ResponseConferenceRoom.from_orm(room)
