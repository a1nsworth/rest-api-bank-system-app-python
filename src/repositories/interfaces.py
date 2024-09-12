from abc import abstractmethod
from typing import Protocol, Iterable, Any
from uuid import UUID

type PrimaryKey = int | str | UUID


class AsyncRepository[TModel](Protocol):
    @abstractmethod
    async def create(self, *entities: TModel): ...

    @abstractmethod
    async def get_by_id(self, pk: PrimaryKey) -> TModel | None: ...

    @abstractmethod
    async def get_many_by_id(self, *pk: PrimaryKey) -> Iterable[TModel | None]: ...

    @abstractmethod
    async def get_all(self) -> Iterable[TModel]: ...

    @abstractmethod
    async def delete_by_id(self, pk: PrimaryKey) -> TModel | None: ...

    @abstractmethod
    async def delete_many_by_id(self, *pk: PrimaryKey) -> Iterable[TModel | None]: ...

    @abstractmethod
    async def update(self, pk: PrimaryKey, **data: dict[str, Any]) -> TModel | None: ...

    @abstractmethod
    async def update_many(
        self, *entities: tuple[PrimaryKey, dict[str, Any]]
    ) -> Iterable[TModel | None]: ...
