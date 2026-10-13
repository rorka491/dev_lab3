from fastcrud import crud_router
from src.models.employee import Employee
from src.di.sqlalchemy import get_session
from src.schemas.employee import EmployeeCreateSchema, EmployeeUpdateSchema

router = crud_router(
    session=get_session,
    model=Employee,
    create_schema=EmployeeCreateSchema,
    update_schema=EmployeeUpdateSchema,
    path="/employees",
    tags=["Employee"],
)