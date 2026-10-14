from datetime import UTC, datetime, timedelta
from sqlalchemy.orm import selectinload
from src.commands.base import AbstractCommand
from src.enums import BookingStatus
from src.models.meeting_room import MeetingRoom
from src.models.user import User
from src.repositories.sqlalchemy.meeting_room import MeetingRoomRepository
from src.repositories.sqlalchemy.office import OfficeRepository
from src.repositories.sqlalchemy.participant import ParticipantRepository
from src.repositories.sqlalchemy.transaction import SQLAlchemyTransaction
from src.schemas.booking import BookingSchema, BookingCreateSchema
from src.models.booking import Booking
from src.repositories.sqlalchemy.booking import BookingRepository


class CreateBookingCommand(AbstractCommand[Booking]):
    def __init__(
        self,
        user: User,
        sqlalhemy_transaction: SQLAlchemyTransaction,
        booking_repo: BookingRepository,
        office_repo: OfficeRepository,
        participant_repo: ParticipantRepository,
        meeting_room_repo: MeetingRoomRepository,
    ) -> None:
        self.user = user
        self.sqlalhemy_transaction = sqlalhemy_transaction
        self.booking_repo = booking_repo
        self.office_repo = office_repo
        self.participant_repo = participant_repo
        self.meeting_room_repo = meeting_room_repo
        

    async def execute(self, data: BookingCreateSchema) -> Booking:
        now = datetime.now(UTC)
        async with self.sqlalhemy_transaction:
            room = await self.meeting_room_repo.get_by_id(
                data.meeting_room_id, 
                options=[selectinload(MeetingRoom.office)]
            )

            if room is None: 
                raise ValueError("Комната не найдена")

            if data.starts_at.time() < room.office.work_start:
                raise ValueError("Время начала бронирования раньше открытия офиса")

            if data.ends_at.time() > room.office.work_end:
                raise ValueError("Время окончания бронирования позже закрытия офиса")

            if len(data.user_ids) > room.capacity:
                raise ValueError("Количество участников превышает вместимость комнаты")

            is_free = await self.booking_repo.is_room_free(
                room_id=room.id,
                starts_at=data.starts_at,
                ends_at=data.ends_at,
            )

            if not is_free:
                raise ValueError("Переговорная занята в выбранное время")
            cancel_deadline = now + timedelta(hours=24)
            if cancel_deadline > data.starts_at:
                cancel_deadline = data.starts_at

            booking = await self.booking_repo.create(
                created_by_id=self.user.id,
                meeting_room_id=room.id,
                starts_at=data.starts_at,
                ends_at=data.ends_at,
                cancel_deadline=cancel_deadline,
                status=BookingStatus.PENDING,
            )

            self.participant_repo.add_booking_participants(
                booking_id=booking.id,
                user_ids=data.user_ids,
            )

            duration = data.ends_at - data.starts_at
            requires_approval = len(data.user_ids) > 10 or duration > timedelta(hours=4)

            
            
            if not requires_approval:
                booking.status = BookingStatus.APPROVED

            return booking
