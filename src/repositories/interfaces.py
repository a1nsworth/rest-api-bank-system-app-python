from abc import abstractmethod
from typing import Protocol, Iterable
from uuid import UUID

type PrimaryKey = int | str | UUID


class AccessRepository[TModel, TPk: PrimaryKey](Protocol):
    @abstractmethod
    async def get(self, pk: TPk) -> TModel | None: ...

    @abstractmethod
    async def get_many(self, *pks: TPk) -> Iterable[TModel]: ...

    @abstractmethod
    async def get_all(self) -> Iterable[TModel]: ...


class CreateRepository(Protocol):
    @abstractmethod
    async def create(self, **attrs): ...


class UpdateRepository[TPk: PrimaryKey](Protocol):
    @abstractmethod
    async def update(self, pk: TPk, **attrs): ...


class DeleteRepository[TPk: PrimaryKey](Protocol):
    @abstractmethod
    async def delete(self, pk: TPk): ...


class CRUDRepository[TModel, TPk: PrimaryKey](
    AccessRepository[TModel, TPk],
    CreateRepository,
    UpdateRepository[TPk],
    DeleteRepository[TPk],
    Protocol,
): ...
