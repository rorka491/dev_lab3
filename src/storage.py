from dataclasses import dataclass, field
from uuid import UUID
from src.models.office_booking.entities import Booking, Employee, Office, MeetingRoom

@dataclass(frozen=True)
class Storage[M]:
    employes: dict[UUID, Employee] = field(default_factory=dict)
    offices: dict[UUID, Office] = field(default_factory=dict)
    meeting_rooms: dict[UUID, MeetingRoom] = field(default_factory=dict)
    bookings: dict[UUID, Booking] = field(default_factory=dict)

    def get(self, model: type[M]) -> dict[UUID, M]:
        return {
            Employee: self.employes,
            Office: self.offices,
            MeetingRoom: self.meeting_rooms,
            Booking: self.bookings,
        }[model]


storage = Storage()