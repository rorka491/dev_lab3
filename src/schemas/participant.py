from uuid import UUID

from pydantic import BaseModel, ConfigDict
from src.enums import ParticipantStatus
from src.schemas.user import UserSchema


class ParticipantSchema(BaseModel):
    user_id: UUID
    user: UserSchema
    status: ParticipantStatus
    
    model_config = ConfigDict(from_attributes=True)

