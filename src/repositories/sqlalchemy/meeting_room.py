from uuid import UUID

from src.models.meeting_room import MeetingRoom
from src.repositories.sqlalchemy.base import BaseSQLAlchemyRepository


class MeetingRoomRepository(BaseSQLAlchemyRepository[MeetingRoom]):
    model = MeetingRoom

    async def create(
        self,
        office_id: UUID,
        name: str,
        capacity: int,
    ) -> MeetingRoom:
        obj = self.model(
            office_id=office_id,
            name=name,
            capacity=capacity,
        )
        return await self.save(obj)