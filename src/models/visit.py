import uuid
from sqlalchemy import Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.entities import Employee
from src.models.base import Base
from src.models.meeting import Meeting


class Visit(Base):
    __tablename__ = 'visits'

    meeting_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("meetings.id")
    )
    employee_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("employees.id")
    )
    meeting: Mapped["Meeting"] = relationship("Meeting")
    employee: Mapped["Employee"] = relationship("Employee")
    has_visit: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False
    )