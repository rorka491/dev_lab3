import uuid
from sqlalchemy import ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.employee import Employee
from src.models.meeting_room import MeetingRoom
from src.models.base import Base
from src.models.meeting_employee import meeting_employees


class Meeting(Base):
    __tablename__ = "meetings"

    mettin_room_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("meeting_rooms.id")
    )
    meeting_room: Mapped["MeetingRoom"] = relationship("MeetingRoom")
    employees: Mapped[list["Employee"]] = relationship(
        secondary=meeting_employees
    )

    # employee_id: Mapped[uuid.UUID] = mapped_column(
    #     ForeignKey("employees.id")
    # )
    # employee: Mapped["Employee"] = relationship("Employee")
    # has_visit: Mapped[bool] = mapped_column(
    #     Boolean,
    #     nullable=False,
    # )
    