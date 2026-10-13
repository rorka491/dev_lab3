from fastapi import APIRouter
from src.api.office import router as office_router
from src.api.employee import router as employee_router
from src.api.meeting_room import router as meeting_room_router
from src.api.auth import router as auth_router

router = APIRouter(prefix="/api/v1")
router.include_router(office_router)
router.include_router(employee_router)
router.include_router(meeting_room_router)
router.include_router(auth_router)