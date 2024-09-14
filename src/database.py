import asyncio

from typing import Protocol
from abc import abstractmethod

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)

import aiosqlite


class AsyncRowSession(Protocol):
    @abstractmethod
    async def commit(self): ...

    @abstractmethod
    async def execute(self, *args, **kwargs): ...

    @abstractmethod
    async def rollback(self): ...


class AsyncDatabaseHelper:
    def __init__(self, url: str, echo: bool = False):
        self.url = url
        self.engine = create_async_engine(
            url=self.url,
            echo=echo,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def get_session(self) -> AsyncRowSession:
        async with self.session_factory() as session:
            yield session


class AsyncSQLIteDatabaseHelper:
    def __init__(self, path_to_db: str):
        self.connection = aiosqlite.connect(path_to_db)

    async def get_session(self) -> aiosqlite.Connection:
        async with self.connection as session:
            yield session


sqlite_db_helper = AsyncDatabaseHelper(
    url="sqlite+aiosqlite:///migrations/main.db", echo=True
)

# async_sqlite_db_helper = AsyncDatabaseHelper("migrations/main.db")


async def make_migration(path_to_tables: str):
    async with aiosqlite.connect("migrations/main.db") as session:
        with open(path_to_tables, "r") as sql_file:
            sql_script = sql_file.read()
        await session.executescript(sql_script)
        await session.commit()


if __name__ == "__main__":
    asyncio.run(make_migration("src/models/models.sql"))
