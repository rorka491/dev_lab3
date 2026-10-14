from datetime import time
from src.models.office import Office
from src.repositories.sqlalchemy.base import BaseSQLAlchemyRepository


class OfficeRepository(BaseSQLAlchemyRepository[Office]):
    model = Office

    async def create(
        self,
        name: str,
        work_start: time,
        work_end: time,
    ) -> Office:
        obj = self.model(
            name=name,
            work_start=work_start,
            work_end=work_end,
        )
        return await self.save(obj)