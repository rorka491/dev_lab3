from pydantic import BaseModel, ConfigDict, Field

from src.enums import UserRole


class UserRegister(BaseModel):
    username: str = Field(min_length=3, max_length=255)
    password: str = Field(min_length=8, max_length=128)
    role: UserRole = UserRole.SUBORDINATE


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    role: UserRole


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"