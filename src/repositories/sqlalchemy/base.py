from typing import Generic, Sequence, TypeVar, get_type_hints
import uuid
import inspect
from typing import Any
from uuid import UUID
from sqlalchemy import inspect as sa_inspect
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Select, delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.base import ExecutableOption
from src.exceptions import ObjectNotFound
from src.models.base import Base


# M = TypeVar("M", bound=Base)


class BaseSQLAlchemyRepository[M: Base]:
    model: type[M]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, *args, **kwargs) -> M: ...
        # self.session.add(obj)
        # await self.session.flush()
        # return obj

    def _get_query(self, *, options: Sequence[ExecutableOption]=()) -> Select[tuple[M]]:
        return select(self.model).options(*options) # type: ignore


    async def get_by_id(
        self, 
        id, 
        *,
        options: Sequence[ExecutableOption]=()
    ) -> M | None:
        stmt = (
            self._get_query(options=options)
            .where(self.model.id == id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() # type: ignore

    async def get_or_raise(self, id: uuid.UUID) -> M:
        obj = await self.session.get(self.model, id)
        if obj is None:
            raise ObjectNotFound(f"{self.model.__name__} not found")
        return obj


    async def get(self, *where) -> M | None:
        result = await self.session.execute(select(self.model).where(*where))
        return result.scalar_one_or_none()

    async def save(self, obj: M) -> M:
        self.session.add(obj)
        await self.session.flush()
        return obj

    async def delete(self, obj: M) -> None:
        await self.session.delete(obj)
        await self.session.flush()

    async def delete_by_id(self, id) -> bool:
        result = await self.session.execute(delete(self.model).where(self.model.id == id))
        await self.session.flush()
        return result.rowcount > 0 # type: ignore

    async def all(self) -> list[M]:
        result = await self.session.execute(select(self.model))
        return list(result.scalars().all())
    