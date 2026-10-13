from datetime import datetime
from uuid import UUID
from pydantic import BaseModel
from src.schemas.meeting_room import MeetingRoomSchema


class BookingSchema(BaseModel):
    id: UUID
    employee_id: UUID
    room_id: UUID
    meeting_room: MeetingRoomSchema | None
    starts_at: datetime
    ends_at: datetime
    participants_count: int




# class BookingCreateSchema(BaseModel)