import logging
from logging import getLogger

from fastapi import FastAPI
from dishka.integrations.fastapi import setup_dishka
from fastapi_pagination import add_pagination
from src.api.routers import router
from src.di.container import container
from src.exception_handlers import setup_exception_handlers
from src.lifespan import lifespan


logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

logger.info("TEST INFO")
logger.warning("TEST WARNING")


app = FastAPI(lifespan=lifespan)
app.include_router(router)
setup_exception_handlers(app)
setup_dishka(container, app)
add_pagination(app)