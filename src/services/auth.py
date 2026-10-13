from uuid import UUID
from src.exceptions import InvalidCredentialsError, UsernameAlreadyExistsError
from src.repositories.sqlalchemy.transaction import SQLAlchemyTransaction
from src.repositories.sqlalchemy.user import UserRepository
from src.schemas.auth import UserLogin, UserRegister
from src.auth.jwt import create_access_token
from src.auth.password_hash import verify_password
from src.enums import UserRole
from src.models.user import User



class AuthService:
    def __init__(
        self, 
        user_repo: UserRepository, 
        sqlalchemy_transaction: SQLAlchemyTransaction
    ) -> None:
        self.user_repo = user_repo
        self.sqlalchemy_transaction = sqlalchemy_transaction

    async def register(self, data: UserRegister) -> User:
        async with self.sqlalchemy_transaction:
            user = await self.user_repo.create(data)
        return user

    async def login(self, data: UserLogin) -> str:
        user = await self.user_repo.get_by_username(
            data.username,
        )
        if user is None or not verify_password(
            data.password,
            user.password_hash,
        ):
            raise InvalidCredentialsError
        return create_access_token(user.id)

    async def get_user(self, user_id: UUID) -> User | None:
        return await self.user_repo.get_or_raise(user_id)