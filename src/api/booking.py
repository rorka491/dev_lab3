from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from dishka.integrations.fastapi import FromDishka, inject
from src.di.sqlalchemy import get_session
from src.enums import BookingStatus
from src.models.booking import Booking
from src.schemas.booking import BookingCreateSchema, BookingSchema, BookingUpdateSchema
from src.commands.booking import CreateBookingCommand
from src.permissions import IsSupervisor, UserAbsencePolicy
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import apaginate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.bookings import BookingsService


router = APIRouter(prefix="/bookings", tags=["Booking"])

@router.post(
    "",
    dependencies=[
        Depends(UserAbsencePolicy(absence_maximum=3, since_days=30))
    ]
)
@inject
async def create(
    data: BookingCreateSchema,
    command: FromDishka[CreateBookingCommand]
):
    return await command.execute(data)



@router.get(
    "",
    dependencies=[Depends(IsSupervisor())],
)
@inject
async def get_pending_bookings(
    service: FromDishka[BookingsService],
    status: Annotated[BookingStatus | None, Query()] = None,
) -> Page[BookingSchema]:
    return await service.paginate(status=status)


@router.patch(
    "/{id}",
    dependencies=[Depends(IsSupervisor())],
)
@inject
async def update(
    id: UUID,
    data: BookingUpdateSchema,
    service: FromDishka[BookingsService],
):
    return await service.update(id, data)
