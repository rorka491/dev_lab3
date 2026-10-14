from fastapi_pagination import Page

from src.enums import BookingStatus
from src.repositories.sqlalchemy.booking import BookingRepository
from src.schemas.booking import BookingSchema
from src.services.base import BaseService

class BookingsService(BaseService[BookingRepository]):

    async def paginate(self, status: BookingStatus | None=None) -> Page[BookingSchema]:
        return await self.repo.paginate(status=status)