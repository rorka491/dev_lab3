from dataclasses import dataclass
from datetime import time, datetime
from uuid import UUID
# from src.models.office_booking.exceptions import InvalidValueObject


@dataclass(frozen=True)
class Base:
    id: UUID


@dataclass(frozen=True)
class Employee(Base):
    full_name: str
    employee_number: str


@dataclass(frozen=True)
class Office(Base):
    name: str
    work_start: time
    work_end: time

    def __post_init__(self):
        if self.work_start >= self.work_end:
            raise InvalidValueObject(
                "work_start must have be before work_end"
            )


@dataclass(frozen=True)
class MeetingRoom(Base):
    office_id: UUID
    name: str
    capacity: int


@dataclass(frozen=True)
class Booking(Base):
    employee_id: UUID
    room_id: UUID
    starts_at: datetime
    ends_at: datetime
    participants_count: int

    def __post_init__(self):
        if self.starts_at >= self.ends_at:
            raise InvalidValueObject(
                "starts_at must have be before ends_at"
            )


# @dataclass(frozen=True)
# class Order()