from dishka import Provider, provide, Scope

from src.commands.booking import CreateBookingCommand
from src.models.user import User
from src.repositories.sqlalchemy.booking import BookingRepository
from src.repositories.sqlalchemy.meeting_room import MeetingRoomRepository
from src.repositories.sqlalchemy.office import OfficeRepository
from src.repositories.sqlalchemy.participant import ParticipantRepository
from src.repositories.sqlalchemy.transaction import SQLAlchemyTransaction



class CommandProvider(Provider):

    @provide(scope=Scope.REQUEST)
    async def create_booking_command(
        self,
        user: User,
        sqlalhemy_transaction: SQLAlchemyTransaction,
        booking_repo: BookingRepository,
        office_repo: OfficeRepository,
        participant_repo: ParticipantRepository,
        meeting_room_repo: MeetingRoomRepository,
    ) -> CreateBookingCommand:
        return CreateBookingCommand(
            user = user,
            sqlalhemy_transaction = sqlalhemy_transaction,
            booking_repo = booking_repo,
            office_repo = office_repo,
            participant_repo = participant_repo,
            meeting_room_repo = meeting_room_repo
        )
    