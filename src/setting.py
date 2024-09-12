from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class DbSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file="../.env")
    user: str = Field(..., alias="POSTGRES_USER")
    password: str = Field(..., alias="POSTGRES_PASSWORD")
    db: str = Field(..., alias="POSTGRES_DB")
    host: int = Field(..., alias="POSTGRES_HOST")
    port: int = Field(..., alias="POSTGRES_PORT")

    @property
    @lru_cache
    def url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.user}:{self.password}@{5433}:{5432}/{self.db}"
        )


@lru_cache
def get_db_setting() -> DbSettings:
    return DbSettings()
