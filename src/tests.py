from datetime import datetime, time
from uuid import uuid4

import pytest

from src.models.office_booking.entities import (
    Booking,
    Employee,
    MeetingRoom,
    Office,
)
from src.models.office_booking.exceptions import InvalidValueObject
from src.models.office_booking.repository import (
    BookingRepository,
    EmployeeRepository,
    MeetingRoomRepository,
    OfficeRepository,
)
from src.models.office_booking.storage import storage


@pytest.fixture(autouse=True)
def clear_storage():
    storage.employes.clear()
    storage.offices.clear()
    storage.meeting_rooms.clear()
    storage.bookings.clear()


# ==================== Office ====================


def test_create_office():
    repository = OfficeRepository()

    office = repository.create(
        name="Office 101",
        work_start=time(9, 0),
        work_end=time(18, 0),
    )

    assert isinstance(office, Office)
    assert office.name == "Office 101"
    assert office.work_start == time(9, 0)
    assert office.work_end == time(18, 0)


# def test_create_office_saves_to_storage():
#     repository = OfficeRepository()

#     office = repository.create(
#         name="Office 101",
#         work_start=time(9, 0),
#         work_end=time(18, 0),
#     )

#     assert repository.save(office) == office


def test_office_work_start_must_be_before_work_end():
    with pytest.raises(InvalidValueObject):
        Office(
            id=uuid4(),
            name="Office 101",
            work_start=time(18, 0),
            work_end=time(9, 0),
        )


def test_office_work_start_cannot_equal_work_end():
    with pytest.raises(InvalidValueObject):
        Office(
            id=uuid4(),
            name="Office 101",
            work_start=time(9, 0),
            work_end=time(9, 0),
        )


def test_get_office_by_id():
    repository = OfficeRepository()

    office = repository.create(
        name="Office 101",
        work_start=time(9, 0),
        work_end=time(18, 0),
    )

    result = repository.get_by_id(office.id)

    assert result == office


def test_get_missing_office():
    repository = OfficeRepository()

    result = repository.get_by_id(uuid4())

    assert result is None




def test_create_employee():
    repository = EmployeeRepository()

    employee = repository.create(
        full_name="Иван Иванов",
        employee_number="EMP-001",
    )

    assert isinstance(employee, Employee)
    assert employee.full_name == "Иван Иванов"
    assert employee.employee_number == "EMP-001"


# def test_create_employee_saves_to_storage():
#     repository = EmployeeRepository()

#     employee = repository.create(
#         full_name="Иван Иванов",
#         employee_number="EMP-001",
#     )

#     assert repository.save(employee) == employee


def test_get_employee_by_id():
    repository = EmployeeRepository()

    employee = repository.create(
        full_name="Иван Иванов",
        employee_number="EMP-001",
    )

    result = repository.get_by_id(employee.id)

    assert result == employee


def test_get_missing_employee():
    repository = EmployeeRepository()

    result = repository.get_by_id(uuid4())

    assert result is None


# ==================== MeetingRoom ====================


def test_create_meeting_room():
    repository = MeetingRoomRepository()
    office_id = uuid4()
    room = repository.create(
        office_id=office_id,
        capacity=10,
        name="Meeting Room A",
    )

    assert isinstance(room, MeetingRoom)
    assert room.office_id == office_id
    assert room.capacity == 10
    assert room.name == "Meeting Room A"


# def test_create_meeting_room_saves_to_storage():
#     repository = MeetingRoomRepository()

#     room = repository.create(
#         office_id=uuid4(),
#         capacity=10,
#         name="Meeting Room A",
#     )

#     assert repository.save(room) == room


def test_get_meeting_room_by_id():
    repository = MeetingRoomRepository()

    room = repository.create(
        office_id=uuid4(),
        capacity=10,
        name="Meeting Room A",
    )

    result = repository.get_by_id(room.id)

    assert result == room


def test_get_missing_meeting_room():
    repository = MeetingRoomRepository()

    result = repository.get_by_id(uuid4())

    assert result is None


# ==================== Booking ====================


def test_create_booking():
    repository = BookingRepository()

    employee_id = uuid4()
    room_id = uuid4()

    starts_at = datetime(2026, 9, 30, 10, 0)
    ends_at = datetime(2026, 9, 30, 11, 0)

    booking = repository.create(
        employee_id=employee_id,
        office_id=uuid4(),
        room_id=room_id,
        starts_at=starts_at,
        ends_at=ends_at,
        participants_count=5,
    )

    assert isinstance(booking, Booking)
    assert booking.employee_id == employee_id
    assert booking.room_id == room_id
    assert booking.starts_at == starts_at
    assert booking.ends_at == ends_at
    assert booking.participants_count == 5


def test_create_booking_saves_to_storage():
    repository = BookingRepository()

    booking = repository.create(
        employee_id=uuid4(),
        office_id=uuid4(),
        room_id=uuid4(),
        starts_at=datetime(2026, 9, 30, 10, 0),
        ends_at=datetime(2026, 9, 30, 11, 0),
        participants_count=5,
    )

    assert storage.bookings[booking.id] == booking


def test_get_booking_by_id():
    repository = BookingRepository()

    booking = repository.create(
        employee_id=uuid4(),
        office_id=uuid4(),
        room_id=uuid4(),
        starts_at=datetime(2026, 9, 30, 10, 0),
        ends_at=datetime(2026, 9, 30, 11, 0),
        participants_count=5,
    )

    result = repository.get_by_id(booking.id)

    assert result == booking


def test_get_missing_booking():
    repository = BookingRepository()

    result = repository.get_by_id(uuid4())

    assert result is None


def test_booking_starts_at_must_be_before_ends_at():
    with pytest.raises(InvalidValueObject):
        Booking(
            id=uuid4(),
            employee_id=uuid4(),
            room_id=uuid4(),
            starts_at=datetime(2026, 9, 30, 11, 0),
            ends_at=datetime(2026, 9, 30, 10, 0),
            participants_count=5,
        )


def test_booking_cannot_have_equal_start_and_end():
    moment = datetime(2026, 9, 30, 10, 0)

    with pytest.raises(InvalidValueObject):
        Booking(
            id=uuid4(),
            employee_id=uuid4(),
            room_id=uuid4(),
            starts_at=moment,
            ends_at=moment,
            participants_count=5,
        )