from fastapi import HTTPException, Request
import jwt
from uuid import UUID
from fastapi import status
from dishka import Scope, Provider, provide
from src.auth.jwt import decode_access_token
from src.models.user import User
from src.repositories.sqlalchemy.user import UserRepository



class UserProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_user_id(self, request: Request) -> UUID:
        authorization = request.headers.get("Authorization")
        if authorization is None or not authorization.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing access token",
            )
        token = authorization.removeprefix("Bearer ")
        try:
            payload = decode_access_token(token)
            user_id = UUID(payload["sub"])
        except (jwt.InvalidTokenError, ValueError, KeyError, TypeError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired access token",
            ) from None
        return user_id



    @provide(scope=Scope.REQUEST)
    async def get_current_user(
        self,
        user_repo: UserRepository, 
        user_id: UUID
    ) -> User:
        return await user_repo.get_or_raise(user_id)

    