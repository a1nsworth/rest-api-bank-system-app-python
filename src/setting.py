from pydantic import Field
from pydantic_settings import BaseSettings


class DbSettings(BaseSettings):
    user: str | None = Field(default=None, alias="DB_USER")
    password: str | None = Field(default=None, alias="DB_PASSWORD")
    db: str | None = Field(default=None, alias="DB_NAME")
    host: int | None = Field(default=None, alias="DB_HOST")
    port: int | None = Field(default=None, alias="DB_PORT")
    engine: str | None = Field(default=None, alias="DB_ENGINE")
    echo: bool | None = Field(True, alias="DB_ECHO")

    @property
    def url(self) -> str:
        if not self.engine:
            return "sqlite+aiosqlite:///migrations/main.db"
        else:
            return f"postgresql+asyncpg://{self.user}:{self.password}@{5433}:{5432}/{self.db}"
