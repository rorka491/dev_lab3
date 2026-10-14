from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.sqlalchemy.booking import BookingRepository
from src.repositories.sqlalchemy.meeting_room import MeetingRoomRepository
from src.repositories.sqlalchemy.office import OfficeRepository
from src.repositories.sqlalchemy.participant import ParticipantRepository
from src.repositories.sqlalchemy.user import UserRepository


class RepositoryProvider(Provider):

    @provide(scope=Scope.REQUEST)
    def user_repository(self, session: AsyncSession) -> UserRepository:
        return UserRepository(session=session)

    @provide(scope=Scope.REQUEST)
    def office_repository(self, session: AsyncSession) -> OfficeRepository:
        return OfficeRepository(session=session)

    @provide(scope=Scope.REQUEST)
    def booking_repository(self, session: AsyncSession) -> BookingRepository:
        return BookingRepository(session=session)

    @provide(scope=Scope.REQUEST)
    def meeting_room_repository(
        self,
        session: AsyncSession,
    ) -> MeetingRoomRepository:
        return MeetingRoomRepository(session=session)

    @provide(scope=Scope.REQUEST)
    def participant_repository(
        self,
        session: AsyncSession,
    ) -> ParticipantRepository:
        return ParticipantRepository(session=session)