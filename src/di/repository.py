from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.sqlalchemy.user import UserRepository

class RepositoryProvider(Provider):

    @provide(scope=Scope.REQUEST)
    def user_repository(self, session: AsyncSession) -> UserRepository:
        return UserRepository(session=session)
    