import uuid
from typing import TYPE_CHECKING
from datetime import date, datetime, timezone
from sqlalchemy import DateTime, Enum, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import Base
from src.enums import BookingStatus


if TYPE_CHECKING:
    from src.models.meeting_room import MeetingRoom
    from src.models.user import User
    from src.models.participant import Participant

class Booking(Base):
    __tablename__ = "bookings"
    meeting_room_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("meeting_rooms.id"),
    )
    meeting_room: Mapped["MeetingRoom"] = relationship("MeetingRoom")
    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    ends_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    # participants_count: Mapped[int] = mapped_column(Integer)
    status: Mapped[BookingStatus] = mapped_column(
        Enum(BookingStatus),
        nullable=False,
    )
    created_by_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )
    created_by: Mapped["User"] = relationship("User")
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
    )

    cancel_deadline: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    participants: Mapped[list["Participant"]] = relationship("Participant")