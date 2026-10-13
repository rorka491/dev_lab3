import uuid
from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column
from src.models.base import Base


class Booking(Base):
    __tablename__ = "bookings"

    employee_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("employees.id"),
    )
    room_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("meeting_rooms.id"),
    )
    starts_at: Mapped[datetime] = mapped_column(DateTime)
    ends_at: Mapped[datetime] = mapped_column(DateTime)
    participants_count: Mapped[int] = mapped_column(Integer)
