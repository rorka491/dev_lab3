import asyncio
from logging import getLogger

from src.di.container import container
from src.repositories.sqlalchemy.booking import BookingRepository

logger = getLogger(__name__)


async def cancel_all_expires_bookings() -> None:
    logger.info("Expired bookings task started")

    while True:
        try:
            async with container() as request_container:
                booking_repo = await request_container.get(BookingRepository)
                await booking_repo.cancel_all_expires()

        except asyncio.CancelledError:
            logger.info("Expired bookings task stopped")
            raise
        except Exception:
            logger.exception("Failed to cancel expired bookings")

        await asyncio.sleep(1)