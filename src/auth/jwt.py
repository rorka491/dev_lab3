from datetime import datetime, timedelta, timezone
from uuid import UUID
from src.core.config import settings
import jwt
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 900


def create_access_token(user_id: UUID) -> str:
    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES,
    )

    payload = {
        "sub": str(user_id),
        "exp": expires_at,
    }

    return jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=ALGORITHM,
    )


def decode_access_token(token: str) -> dict:
    return jwt.decode(
        token,
        settings.JWT_SECRET_KEY,
        algorithms=[ALGORITHM],
    )