from fastapi import FastAPI
from dishka.integrations.fastapi import setup_dishka
from src.api.routers import router
from src.di.container import container


app = FastAPI()
app.include_router(router)
setup_dishka(container, app)