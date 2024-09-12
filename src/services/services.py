from typing import Iterable

from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.repositories import SQLAlchemyAsyncRepository
from src.models.models import Base

from src.repositories.repositories import PrimaryKey


class BaseAsyncCRUDService[
    TModel: Base, TRepository: SQLAlchemyAsyncRepository
]:
    def __init__(self, session: AsyncSession, repository: TRepository):
        self._session = session
        self._repository = repository

    async def create(self, *model: TModel):
        await self._repository.create(*model)
        await self._session.commit()

    async def get_by_id(self, pk: PrimaryKey) -> TModel | None:
        return await self._repository.get_by_id(pk)

    async def get_all(self) -> Iterable[TModel]:
        return await self._repository.get_all()

    async def delete_by_id(self, pk: PrimaryKey) -> TModel | None:
        result = await self._repository.delete_by_id(pk)
        await self._session.commit()
        return result

    async def update(self, pk: PrimaryKey, model: TModel) -> TModel | None:
        result = await self._repository.update(pk, **model)
        await self._session.commit()
        return result
