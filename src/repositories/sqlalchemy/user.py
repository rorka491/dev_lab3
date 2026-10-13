from sqlalchemy import select

from src.exceptions import ObjectNotFound
from src.repositories.sqlalchemy.base import BaseSQLAlchemyRepository
from src.models.user import User
from src.schemas.auth import UserRegister
from src.auth.password_hash import hash_password


class UserRepository(BaseSQLAlchemyRepository[User]):
    model = User

    async def create(self, data: UserRegister) -> User:
        password_hash = hash_password(data.password)
        user = self.model(
            username=data.username,
            role=data.role,
            password_hash=password_hash
        )
        return await self.save(user)


    async def get_by_username(self, username: str) -> User:
        stmt = select(self.model).where(self.model.username==username)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()
        if user is None:
            raise ObjectNotFound(f"User with username '{username}' not found")  
        return user

    