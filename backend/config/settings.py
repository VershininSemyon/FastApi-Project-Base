
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        case_sensitive=True,
    )

    UVICORN_RELOAD: bool = False
    UVICORN_WORKERS_COUNT: int = 4

    POSTGRES_DB_NAME: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str = 'postgres'
    POSTGRES_PORT: int = 5432

    JWT_ALGORITHM: str = 'HS256'
    JWT_SIGNING_KEY: str
    ACCESS_TOKEN_LIFETIME_MINUTES: int = 15
    REFRESH_TOKEN_LIFETIME_DAYS: int = 2

    PASSWORD_SALT: str

    REDIS_PASSWORD: str
    REDIS_PORT: int = 6379

    RATE_LIMIT_REQUESTS_LIMIT: int = 25
    RATE_LIMIT_WINDOW_SECONDS: int = 60

    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB_NAME}"

    @property
    def redis_url(self) -> str:
        return f"redis://:{self.REDIS_PASSWORD}@redis:{self.REDIS_PORT}/0"


settings = Settings()
