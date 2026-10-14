import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.tasks import cancel_all_expires_bookings


@pytest.mark.asyncio
async def test_cancel_all_expires_bookings_calls_repository():
    repository = MagicMock()
    repository.cancel_all_expires = AsyncMock()

    request_container = MagicMock()
    request_container.get = AsyncMock(return_value=repository)

    container_context = MagicMock()
    container_context.__aenter__ = AsyncMock(return_value=request_container)
    container_context.__aexit__ = AsyncMock(return_value=False)

    with (
        patch("src.tasks.container", return_value=container_context),
        patch("src.tasks.asyncio.sleep", new_callable=AsyncMock) as sleep,
    ):
        sleep.side_effect = asyncio.CancelledError

        with pytest.raises(asyncio.CancelledError):
            await cancel_all_expires_bookings()

    repository.cancel_all_expires.assert_awaited_once()
    request_container.get.assert_awaited_once()
    assert request_container.get.await_args.args[0].__name__ == "BookingRepository"


@pytest.mark.asyncio
async def test_cancel_all_expires_bookings_continues_after_error():
    repository = MagicMock()
    repository.cancel_all_expires = AsyncMock(
        side_effect=[RuntimeError("Database error"), None]
    )

    request_container = MagicMock()
    request_container.get = AsyncMock(return_value=repository)

    container_context = MagicMock()
    container_context.__aenter__ = AsyncMock(return_value=request_container)
    container_context.__aexit__ = AsyncMock(return_value=False)

    with (
        patch("src.tasks.container", return_value=container_context),
        patch("src.tasks.asyncio.sleep", new_callable=AsyncMock) as sleep,
        patch("src.tasks.logger") as logger,
    ):
        sleep.side_effect = [None, asyncio.CancelledError]

        with pytest.raises(asyncio.CancelledError):
            await cancel_all_expires_bookings()

    assert repository.cancel_all_expires.await_count == 2
    logger.exception.assert_called_once_with(
        "Failed to cancel expired bookings"
    )


@pytest.mark.asyncio
async def test_cancel_all_expires_bookings_propagates_cancellation():
    with (
        patch("src.tasks.container") as mocked_container,
        patch("src.tasks.logger"),
    ):
        mocked_container.side_effect = asyncio.CancelledError

        with pytest.raises(asyncio.CancelledError):
            await cancel_all_expires_bookings()

    mocked_container.assert_called_once_with()