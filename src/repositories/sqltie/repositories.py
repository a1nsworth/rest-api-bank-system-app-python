from pypika import Table, Query, SQLLiteQuery
from typing import Any, Iterable

from src.repositories.interfaces import AsyncRepository, PrimaryKey
from src.models.sqlmodels import Bank

from aiosqlite.core import Connection


class BankRepository(AsyncRepository[Bank]):
    def __init__(self, connection: Connection) -> None:
        self._connection = connection
        self._table = Table("bank")

    async def create(self, *entities: Bank):
        stmt = (
            SQLLiteQuery.into(self._table)
            .columns(self._table.name)
            .insert(((entities.name,) for entities in entities))
        )
        self._connection.execute(stmt.get_sql())

    async def get_by_id(self, pk: PrimaryKey) -> Bank | None:
        pass

    async def get_many_by_id(self, *pk: PrimaryKey) -> Iterable[Bank | None]:
        pass

    async def get_all(self) -> Iterable[Bank]:
        pass

    async def delete_by_id(self, pk: PrimaryKey) -> Bank | None:
        pass

    async def delete_many_by_id(self, *pk: PrimaryKey) -> Iterable[Bank | None]:
        pass

    async def update(self, pk: PrimaryKey, **data: dict[str, Any]) -> Bank | None:
        pass

    async def update_many(
        self, *entities: tuple[PrimaryKey, dict[str, Any]]
    ) -> Iterable[Bank | None]:
        pass


async def main():
    from database import async_sqlite_db_helper

    session = async_sqlite_db_helper.get_session()
    b = BankRepository(session)
    await b.create(Bank("VTB"))
    session.commit()


if __name__ == "__main__":
    main()
