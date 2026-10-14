from datetime import UTC, datetime
from uuid import UUID
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import apaginate
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload
from src.enums import BookingStatus
from src.models.booking import Booking
from src.repositories.sqlalchemy.base import BaseSQLAlchemyRepository
from src.schemas.booking import BookingSchema


class BookingRepository(BaseSQLAlchemyRepository[Booking]):
    model = Booking

    async def create(
        self,
        created_by_id: UUID,
        meeting_room_id: UUID,
        starts_at: datetime,
        ends_at: datetime,
        cancel_deadline: datetime,
        status: BookingStatus
    ) -> Booking:
        obj = self.model(
            created_by_id=created_by_id,
            meeting_room_id=meeting_room_id,
            starts_at=starts_at,
            ends_at=ends_at,
            cancel_deadline=cancel_deadline,
            status=status,
        )
        return await self.save(obj)


    async def is_room_free(
        self,
        room_id: UUID,
        starts_at: datetime,
        ends_at: datetime,
    ) -> bool:
        stmt = select(self.model.id).where(
            Booking.meeting_room_id == room_id,
            Booking.starts_at < ends_at,
            Booking.ends_at > starts_at,
            Booking.status.in_(
                [
                    BookingStatus.APPROVED,
                ]
            ),
        ).limit(1)

        result = await self.session.scalar(stmt)
        return result is None


    async def paginate(self, status: BookingStatus | None=None) -> Page[BookingSchema]:
        query = self._get_query(options=[selectinload(self.model.participants)])
        if status is not None:
            query = query.where(Booking.status == status)
        query = query.order_by(Booking.created_at, Booking.id)
        
        return await apaginate(self.session, query)

    async def cancel_all_expires(self) -> None:
        stmt = (
            update(self.model)
            .where(
                self.model.cancel_deadline <= datetime.now(UTC),
                self.model.status == BookingStatus.PENDING,
            )
            .values(status=BookingStatus.CANCEL)
        )
        await self.session.execute(stmt)
        await self.session.commit()


