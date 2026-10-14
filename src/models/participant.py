import uuid
from typing import TYPE_CHECKING
from sqlalchemy import Enum, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import Base
from src.models.booking import Booking
from src.enums import ParticipantStatus 

if TYPE_CHECKING:
    from src.models.user import User

class Participant(Base):
    __tablename__ = 'participants'
    __table_args__ = (
        UniqueConstraint(
            "booking_id",
            "user_id",
            name="uq_participant_booking_user",
        ),
    )

    booking_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("bookings.id"),
        nullable=False,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )
    booking: Mapped["Booking"] = relationship("Booking")
    user: Mapped["User"] = relationship("User")
    status: Mapped[ParticipantStatus] = mapped_column(
        Enum(ParticipantStatus),
        nullable=False 
    )

    