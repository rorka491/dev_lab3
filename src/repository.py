from datetime import datetime, time
from typing import Any, Protocol
from uuid import UUID, uuid4
from src.models.office_booking.entities import Booking, Employee, MeetingRoom, Office
from src.models.office_booking.storage import storage


class Repository[M](Protocol):
    def create(self, *args, **kwargs) -> M: ...

    def get_by_id(self, id: UUID) -> M | None: ...

    def save(self, obj: M) -> M: ...


class BaseRepository[M]:
    model: type[M]

    def create(self, *args, **kwargs) -> M: ...

    def save(self, obj: M) -> M:
        storage.get(self.model)[obj.id] = obj # type: ignore
        return obj

    def get_by_id(self, id: UUID) -> M | None:
        return storage.get(self.model).get(id)


class EmployeeRepository(BaseRepository[Employee]):
    model = Employee

    def create(self, full_name: str, employee_number: str) -> Employee:
        employee = Employee(
            id=uuid4(),
            full_name=full_name,
            employee_number=employee_number,
        )
        return self.save(employee)


class OfficeRepository(BaseRepository[Office]):
    model = Office

    def create(
        self, 
        name: str, 
        work_start: time, 
        work_end: time
    ) -> Office:
        office = Office(
            id=uuid4(),
            name=name,
            work_start=work_start,
            work_end=work_end
        )
        return self.save(office)


class MeetingRoomRepository(BaseRepository[MeetingRoom]):
    model = MeetingRoom

    def create(self, office_id: UUID, capacity: int, name: str) -> MeetingRoom:
        meeting_room = self.model(
            id=uuid4(),
            office_id=office_id,
            name=name,
            capacity=capacity
        )
        return self.save(meeting_room)

class BookingRepository(BaseRepository[Booking]):
    model = Booking

    def create(self, employee_id: UUID, office_id: UUID, room_id: UUID, ends_at: datetime, starts_at: datetime, participants_count: int) -> Booking:
        booking = self.model(
            id=uuid4(),
            employee_id=employee_id,
            room_id=room_id,
            ends_at=ends_at,
            starts_at=starts_at,
            participants_count=participants_count
        )
        return self.save(booking)