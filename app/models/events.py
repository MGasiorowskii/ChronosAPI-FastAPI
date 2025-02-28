import uuid
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

from models.rooms import ConferenceRoom


class CalendarEventParticipants(SQLModel, table=True):
    event_id: int = Field(foreign_key="calendarevent.id", primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", primary_key=True)


class CalendarEvent(SQLModel, table=True):
    id: int | None = Field(default_factory=None, primary_key=True)
    event_name: str = Field(max_length=255)
    agenda: str
    start: datetime
    end: datetime

    owner_id: uuid.UUID = Field(foreign_key="user.id", ondelete="CASCADE")
    owner: "User" = Relationship(back_populates="owned_events")

    location_id: int | None = Field(
        default=None, foreign_key="conferenceroom.id", ondelete="SET NULL"
    )
    location: "ConferenceRoom" = Relationship(back_populates="events")

    participants: list["User"] = Relationship(
        back_populates="participating_events", link_model=CalendarEventParticipants
    )
