import uuid
from datetime import datetime, time
from sqlalchemy import DateTime, ForeignKey, Integer, String, Time, Uuid
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from src.models.base import Base


class Office(Base):
    __tablename__ = "offices"

    name: Mapped[str] = mapped_column(String(255))
    work_start: Mapped[time] = mapped_column(Time)
    work_end: Mapped[time] = mapped_column(Time)
