from datetime import UTC, datetime
from uuid import UUID
from pydantic import BaseModel, Field, model_validator
from src.schemas.meeting_room import MeetingRoomSchema
from src.schemas.participant import ParticipantSchema
from src.enums import BookingStatus

class BookingSchema(BaseModel):
    id: UUID
    meeting_room_id: UUID
    meeting_room: MeetingRoomSchema | None
    participants: list[ParticipantSchema]
    starts_at: datetime
    ends_at: datetime
    status: BookingStatus



class BookingCreateSchema(BaseModel):
    meeting_room_id: UUID
    user_ids: list[UUID] = Field(min_length=1)
    starts_at: datetime
    ends_at: datetime


    @model_validator(mode="after")
    def validate_booking(self) -> "BookingCreateSchema":
        if self.starts_at >= self.ends_at:
            raise ValueError(
                "Время начала должно быть раньше времени окончания"
            )
        if self.starts_at <= datetime.now(UTC):
            raise ValueError(
                "Нельзя забронировать комнату на прошедшее время"
            )
        if len(self.user_ids) != len(set(self.user_ids)):
            raise ValueError(
                "Список участников содержит дубликаты"
            )

        return self


class BookingUpdateSchema(BaseModel):
    status: BookingStatus