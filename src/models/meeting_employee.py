from sqlalchemy import Column, ForeignKey, Table
from src.models.base import Base


meeting_employees = Table(
    "meeting_employees",
    Base.metadata,
    Column(
        "meeting_id",
        ForeignKey("meetings.id"),
        primary_key=True,
    ),
    Column(
        "employee_id",
        ForeignKey("employees.id"),
        primary_key=True,
    ),
)