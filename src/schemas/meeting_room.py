from datetime import datetime
from uuid import UUID
from pydantic import BaseModel
from src.schemas.office import OfficeSchema


class MeetingRoomSchema(BaseModel):
    id: UUID
    office_id: UUID
    office: OfficeSchema | None
    name: str
    capacity: int


class MettingRoomCreateSchema(BaseModel):
    office_id: UUID
    name: str
    capacity: int


class MettingRoomUpdateSchema(BaseModel):
    office_id: UUID | None
    name: str | None
    capacity: int | None