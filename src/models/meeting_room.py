from sqlalchemy import UUID, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import Base
from src.models.office import Office

class MeetingRoom(Base):
    __tablename__ = "meeting_rooms"
    office_id: Mapped[UUID] = mapped_column(
        ForeignKey("offices.id"),
    )
    office: Mapped["Office"] = relationship("Office")
    name: Mapped[str] = mapped_column(String(255))
    capacity: Mapped[int] = mapped_column(Integer)