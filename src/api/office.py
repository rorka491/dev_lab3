from fastapi import Depends
from fastcrud import crud_router
from src.models.office import Office
from src.di.sqlalchemy import get_session
from src.permissions import IsSupervisor
from src.schemas.office import OfficeCreateSchema, OfficeUpdateSchema


base_dependency = [IsSupervisor(), ]

router = crud_router(
    session=get_session,
    model=Office,
    create_schema=OfficeCreateSchema,
    update_schema=OfficeUpdateSchema,
    path="/offices",
    tags=["Office"],
    create_deps=base_dependency,
    read_deps=base_dependency,
    update_deps=base_dependency,
    delete_deps=base_dependency,
)