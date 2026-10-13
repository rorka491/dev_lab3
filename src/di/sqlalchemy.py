from dishka import Provider, Scope, provide
from collections.abc import AsyncIterable
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from dishka.integrations.fastapi import FromDishka, inject
from src.repositories.sqlalchemy.transaction import SQLAlchemyTransaction
from src.core.config import settings

class SQLAlchemyProvider(Provider):
    @provide(scope=Scope.APP)
    def engine(self) -> AsyncEngine:
        return create_async_engine(settings._postgres_url)

    @provide(scope=Scope.APP)
    def session_factory(
        self,
        engine: AsyncEngine,
    ) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(
            bind=engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    @provide(scope=Scope.REQUEST)
    async def sqlalchemy_session(
        self,
        session_factory: async_sessionmaker[AsyncSession],
    ) -> AsyncIterable[AsyncSession]: # type: ignore
        async with session_factory() as session:
            yield session # type: ignore

    @provide(scope=Scope.REQUEST)
    def sqlalchemy_transaction(self, session: AsyncSession) -> SQLAlchemyTransaction:
        return SQLAlchemyTransaction(session=session)


@inject
def get_session(session: FromDishka[AsyncSession]):
    yield session