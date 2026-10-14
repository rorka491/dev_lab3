import logging
from logging import getLogger
from fastapi import FastAPI
from pathlib import Path
from dishka.integrations.fastapi import setup_dishka
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi_pagination import add_pagination
from src.api.routers import router
from src.di.container import container
from src.exception_handlers import setup_exception_handlers
from src.lifespan import lifespan
from fastapi.middleware.cors import CORSMiddleware


logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

logger.info("TEST INFO")
logger.warning("TEST WARNING")

BASE_DIR = Path(__file__).resolve().parent


app = FastAPI(lifespan=lifespan)

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR),
    name="static",
)

@app.get("/", include_in_schema=False)
async def index() -> FileResponse:
    return FileResponse(BASE_DIR / "index.html")


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:8000",
        "http://localhost:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)
setup_exception_handlers(app)
setup_dishka(container, app)
add_pagination(app)