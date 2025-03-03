import uuid

from pydantic import EmailStr
from sqlmodel import SQLModel, Field, Relationship


class RoomBase(SQLModel):
    name: str = Field(max_length=255)
    address: str = Field(max_length=255)


class ResponseConferenceRoom(RoomBase):
    id: int
    manager: EmailStr

    @classmethod
    def from_orm(cls, room, **kwargs):
        return cls(
            id=room.id,
            name=room.name,
            address=room.address,
            manager=room.manager.email if room.manager else None,
        )


class CreateConferenceRoom(RoomBase):
    manager: EmailStr


class ConferenceRoom(RoomBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    manager_id: uuid.UUID | None = Field(
        default=None, foreign_key="user.id", ondelete="SET NULL"
    )

    manager: "User" = Relationship(back_populates="managed_rooms")
    events: list["CalendarEvent"] = Relationship(back_populates="location")
