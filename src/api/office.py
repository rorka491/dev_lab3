from fastcrud import crud_router
from src.models.office import Office
from src.di.sqlalchemy import get_session
from src.schemas.office import OfficeCreateSchema, OfficeUpdateSchema

router = crud_router(
    session=get_session,
    model=Office,
    create_schema=OfficeCreateSchema,
    update_schema=OfficeUpdateSchema,
    path="/offices",
    tags=["Office"],
)