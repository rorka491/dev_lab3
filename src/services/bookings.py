from uuid import UUID

from fastapi_pagination import Page

from src.enums import BookingStatus
from src.models.booking import Booking
from src.repositories.sqlalchemy.booking import BookingRepository
from src.repositories.sqlalchemy.transaction import SQLAlchemyTransaction
from src.schemas.booking import BookingSchema, BookingUpdateSchema
from src.services.base import BaseService

class BookingsService(BaseService[BookingRepository]):

    def __init__(self, sqlalchemy_transaction: SQLAlchemyTransaction, repo: BookingRepository) -> None:
        self.sqlalchemy_transaction = sqlalchemy_transaction
        super().__init__(repo)

    async def paginate(self, status: BookingStatus | None=None) -> Page[BookingSchema]:
        return await self.repo.paginate(status=status)

    async def update(self, id: UUID, data: BookingUpdateSchema) -> Booking:
        async with self.sqlalchemy_transaction: 
            booking = await self.repo.get_or_raise(id)
            booking.status = data.status
        return await self.repo.save(booking)