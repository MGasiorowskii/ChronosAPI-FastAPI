import uuid
from enum import Enum
from typing import ClassVar
from zoneinfo import available_timezones

from pydantic import EmailStr, field_validator, ValidationError
from sqlmodel import Field, SQLModel

from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


TimezoneEnum = Enum("TimezoneEnum", {tz: tz for tz in available_timezones()}, type=str)


class UserBase(SQLModel):
    company_id: uuid.UUID = Field(default_factory=uuid.uuid4, nullable=False)
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    timezone: TimezoneEnum = Field(default=TimezoneEnum.UTC)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)

    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.password)


class UserCreate(UserBase):
    MAX_PASSWORD_LENGTH: ClassVar[int] = 40
    password: str = Field(min_length=8)

    @field_validator("password", mode="before")  # type: ignore[prop-decorator]
    @classmethod
    def hash_password(cls, value: str) -> str:
        if not pwd_context.identify(value):
            if len(value) > cls.MAX_PASSWORD_LENGTH:
                raise ValidationError(
                    f"Password has to be at most {cls.MAX_PASSWORD_LENGTH} characters long"
                )
            return pwd_context.hash(value)
        return value


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    password: str
