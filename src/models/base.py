import uuid
from datetime import datetime, time
from sqlalchemy import DateTime, ForeignKey, Integer, String, Time, Uuid
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase): 
    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4,
    )
    