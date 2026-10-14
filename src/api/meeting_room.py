from fastcrud import crud_router
from fastapi import APIRouter
from src.di.sqlalchemy import get_session
from src.models.meeting_room import MeetingRoom
from src.permissions import IsSupervisor
from src.schemas.meeting_room import MettingRoomCreateSchema, MettingRoomUpdateSchema

base_dependency = [IsSupervisor(), ]

router = crud_router(
    session=get_session,
    model=MeetingRoom,
    create_schema=MettingRoomCreateSchema,
    update_schema=MettingRoomUpdateSchema,
    path="/meeting-rooms",
    tags=["Metting Room"],
    create_deps=base_dependency,
    read_deps=base_dependency,
    update_deps=base_dependency,
    delete_deps=base_dependency,
)

