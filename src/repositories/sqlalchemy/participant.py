from datetime import datetime
from uuid import UUID

from sqlalchemy import func, select
from src.enums import ParticipantStatus
from src.models.booking import Booking
from src.models.participant import Participant
from src.repositories.sqlalchemy.base import BaseSQLAlchemyRepository


class ParticipantRepository(BaseSQLAlchemyRepository[Participant]):
    model = Participant

    async def create(
        self,
        booking_id: UUID,
        user_id: UUID,
        status: ParticipantStatus,
    ) -> Participant:
        obj = self.model(
            booking_id=booking_id,
            user_id=user_id,
            status=status,
        )
        return await self.save(obj)


    async def count_absences(
        self,
        user_id: UUID,
        since: datetime,
    ) -> int:
        stmt = (
            select(func.count(self.model.id))
            .join(Booking, Participant.booking_id == Booking.id)
            .where(
                self.model.user_id == user_id,
                Participant.status == ParticipantStatus.ABSENT,
                Booking.starts_at >= since,
            )
        )
        result = await self.session.scalar(stmt)
        return result or 0


    def add_booking_participants(self, user_ids: list[UUID], booking_id: UUID):
        for user_id in user_ids:
            participant = self.model(
                booking_id=booking_id,
                user_id=user_id,
                status=ParticipantStatus.PENDING,
            )
            self.session.add(participant)
