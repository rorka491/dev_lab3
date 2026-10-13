from pydantic import BaseModel
from uuid import UUID
from src.schemas.user import UserSchema

class EmployeeSchema(BaseModel):
    id: UUID
    user_id: UUID
    user: UserSchema | None
    full_name: str
    employee_number: str

class EmployeeCreateSchema(BaseModel):
    user_id: UUID
    full_name: str
    employee_number: str

class EmployeeUpdateSchema(BaseModel):
    full_name: str | None
    employee_number: str | None