import uuid

from sqlmodel import SQLModel, Field, Relationship


class ConferenceRoom(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=255)
    address: str = Field(max_length=255)

    manager_id: uuid.UUID | None = Field(
        default=None, foreign_key="user.id", ondelete="SET NULL"
    )
    manager: "User" = Relationship(back_populates="managed_rooms")
    events: list["CalendarEvent"] = Relationship(back_populates="location")
