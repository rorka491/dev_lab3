from typing import TYPE_CHECKING
from sqlalchemy import String, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import Base
from src.enums import UserRole


class User(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True
    )
    password_hash: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole),
        nullable=False,
    )