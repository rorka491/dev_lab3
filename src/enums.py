from enum import StrEnum


class UserRole(StrEnum):
    SUPERVISOR = "supervisor"
    SUBORDINATE = "subordinate"
    ADMIN = "admin"


class BookingStatus(StrEnum):
    PENDING = "pending"
    APPROVED = "approved"
    CANCEL = "cancel"


class ParticipantStatus(StrEnum):
    PENDING = "pending"
    PRESENT = "present"
    ABSENT = "absent"