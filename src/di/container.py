from dishka import make_async_container
from dishka.integrations.fastapi import FastapiProvider 
from src.di.command import CommandProvider
from src.di.service import ServiceProvider
from src.di.sqlalchemy import SQLAlchemyProvider
from src.di.repository import RepositoryProvider
from src.di.user import UserProvider

container = make_async_container(
    CommandProvider(),
    SQLAlchemyProvider(),
    UserProvider(),
    RepositoryProvider(),
    ServiceProvider(),
    FastapiProvider(),
)