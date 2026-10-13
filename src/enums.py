from enum import StrEnum



class UserRole(StrEnum):
    SUPERVISOR = "supervisor"
    SUBORDINATE = "subordinate"
    ADMIN = "admin"
