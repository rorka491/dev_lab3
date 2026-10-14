import asyncio
from contextlib import asynccontextmanager
from logging import getLogger
from fast_depends import inject
from fastapi import FastAPI
from src.tasks import cancel_all_expires_bookings

logger = getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Lifespan started")
    cancel_expires = asyncio.create_task(cancel_all_expires_bookings())
    
    try:
        yield 
    finally:
        cancel_expires.cancel()
        await asyncio.gather(
            cancel_expires,
            return_exceptions=True,
        )