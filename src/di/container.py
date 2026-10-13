from dishka import make_async_container
from src.di.service import ServiceProvider
from src.di.sqlalchemy import SQLAlchemyProvider
from src.di.repository import RepositoryProvider

container = make_async_container(
    SQLAlchemyProvider(),
    RepositoryProvider(),
    ServiceProvider(),
)