from datetime import UTC, datetime, timedelta
from typing import Any
from dishka.integrations.fastapi import inject, FromDishka

from src.models.user import User
from src.repositories.sqlalchemy.participant import ParticipantRepository
from src.enums import UserRole



class UserAbsencePolicy:
    def __init__(
        self,
        absence_maximum: int,
        since_days: int
    ) -> None:
        self.absence_maximum = absence_maximum
        self.since_days = since_days

    @inject
    async def __call__(
        self, 
        user: FromDishka[User],
        participant_repo: FromDishka[ParticipantRepository]
    ) -> Any:
        now = datetime.now(UTC)
        count = await participant_repo.count_absences(
            user_id=user.id,
            since=now - timedelta(days=30),
        )
        if count >= self.absence_maximum:
            raise ValueError(f"Пользователь не может сделать бронь имея больше {self.absence_maximum} за послдение {self.since_days}")


class IsSupervisor:
    
    @inject
    async def __call__(self, user: FromDishka[User]) -> Any:
        if not user.role == UserRole.SUPERVISOR:
            raise ValueError("Пользователь не руководитель")