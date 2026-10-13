from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, HTTPException, status

from src.models.user import User
from src.schemas.auth import (
    TokenResponse,
    UserLogin,
    UserRegister,
    UserResponse,
)
from src.services.auth import (
    AuthService,
)
from src.exceptions import InvalidCredentialsError, UsernameAlreadyExistsError

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
@inject
async def register(
    data: UserRegister,
    service: FromDishka[AuthService]
):
    try:
        return await service.register(data)
    except UsernameAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists",
        ) from None


@router.post(
    "/login",
    response_model=TokenResponse,
)
@inject
async def login(
    data: UserLogin,
    service: FromDishka[AuthService]
) -> TokenResponse:
    try:
        token = await service.login(data)
    except InvalidCredentialsError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        ) from None

    return TokenResponse(access_token=token)


@router.get(
    "/me",
    response_model=UserResponse,
)
@inject
async def get_me(
    user: FromDishka[User],
) -> User:
    return user