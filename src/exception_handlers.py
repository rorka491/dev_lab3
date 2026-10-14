
from fastapi import FastAPI, HTTPException, Request

from src.exceptions import ObjectNotFound


def setup_exception_handlers(app: FastAPI) -> None:

    @app.exception_handler(ValueError)
    async def value_error(
        request: Request,
        exc: ValueError,
    ):
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    @app.exception_handler(ObjectNotFound)
    async def object_not_found_handler(
        request: Request,
        exc: ObjectNotFound,
    ):
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )