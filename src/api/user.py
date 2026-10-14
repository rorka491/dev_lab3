from fastapi import Depends
from fastcrud import crud_router
from src.models.office import Office
from src.di.sqlalchemy import get_session
from src.models.user import User
from src.permissions import IsSupervisor



base_dependency = [IsSupervisor(), ]

router = crud_router(
    session=get_session,
    model=User,
    create_schema=...,
    update_schema=..., 
    path="/users",
    tags=["User"],
    create_deps=base_dependency,
    read_deps=base_dependency,
    update_deps=base_dependency,
    delete_deps=base_dependency,
    deleted_methods=["create", "update"],
)