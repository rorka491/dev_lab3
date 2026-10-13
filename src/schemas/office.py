from datetime import datetime, time
from uuid import UUID
from pydantic import BaseModel


class OfficeSchema(BaseModel):
    id: UUID
    name: str
    work_start: time
    work_end: time


class OfficeCreateSchema(BaseModel):
    name: str
    work_start: time
    work_end: time

class OfficeUpdateSchema(BaseModel):
    name: str | None
    work_start: time | None
    work_end: time | None
