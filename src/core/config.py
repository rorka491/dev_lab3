from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    JWT_SECRET_KEY: str

    POSTGRES_NAME: str = "postgres"
    POSTGRES_PORT: int = 5432
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_USER: str = "postgres"
    POSTGRES_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"

    @property
    def _postgres_url(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_NAME}"



settings = Settings()