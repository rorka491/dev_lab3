from fastcrud import crud_router
from fastapi import APIRouter
from src.di.sqlalchemy import get_session
from src.models.meeting_room import MeetingRoom
from src.schemas.meeting_room import MettingRoomCreateSchema, MettingRoomUpdateSchema

router = crud_router(
    session=get_session,
    model=MeetingRoom,
    create_schema=MettingRoomCreateSchema,
    update_schema=MettingRoomUpdateSchema,
    path="/meeting-room",
    tags=["Metting Room"],
)

