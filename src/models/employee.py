import uuid
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import Base
from src.models.user import User


class Employee(Base):
    __tablename__ = "employees"

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"),
    )
    user: Mapped["User"] = relationship("User")
    full_name: Mapped[str] = mapped_column(String(255))
    employee_number: Mapped[str] = mapped_column(
        String(50), 
        unique=True
    )