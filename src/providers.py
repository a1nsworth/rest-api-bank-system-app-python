from typing import AsyncIterable

from dishka import Provider, provide, Scope
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, AsyncEngine, create_async_engine

from src.setting import DbSettings


class DbSettingProvider(Provider):
    @provide(scope=Scope.APP)
    def get_setting(self) -> DbSettings:
        return DbSettings()


class AsyncDatabaseProvider(Provider):
    @provide(scope=Scope.APP)
    def get_async_engine(self, setting: DbSettings) -> AsyncEngine:
        return create_async_engine(url=setting.url, echo=setting.echo)

    @provide(scope=Scope.APP)
    def get_session_factory(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(
            bind=engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False)

    @provide(scope=Scope.REQUEST)
    async def get_async_session(self, factory: async_sessionmaker[AsyncSession]) -> AsyncIterable[AsyncSession]:
        async with factory() as session:
            yield session
