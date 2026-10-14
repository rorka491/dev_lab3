
from fastapi import FastAPI, HTTPException, Request


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