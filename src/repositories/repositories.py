from abc import ABC
from operator import attrgetter
from typing import Iterable, Any

from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import banks as models
from src.models.models import Base
from src.repositories.interfaces import AsyncRepository, PrimaryKey


class SQLAlchemyAsyncRepository[TModel: Base](AsyncRepository[TModel], ABC):
    __pk_name__ = "id"
    __model__: TModel

    def __init__(self, session: AsyncSession):
        self._session = session
        if self.__model__ is None:
            raise ValueError("__model__ must be defined")

    async def create(self, *entities: TModel):
        self._session.add_all(entities)

    async def get_by_id(self, pk: PrimaryKey) -> TModel | None:
        stmt = select(self.__model__).where(
            attrgetter(self.__pk_name__)(self.__model__) == pk
        )
        return (await self._session.scalars(stmt)).unique().one_or_none()

    async def get_many_by_id(self, *pk: PrimaryKey) -> Iterable[TModel]:
        stmt = select(self.__model__).where(
            attrgetter(self.__pk_name__)(self.__model__) == pk
        )
        return (await self._session.scalars(stmt)).unique().all()

    async def get_all(self) -> Iterable[TModel]:
        stmt = select(self.__model__)
        return (await self._session.scalars(stmt)).unique().all()

    async def delete_by_id(self, pk: PrimaryKey) -> TModel | None:
        stmt = (
            delete(self.__model__)
            .where(attrgetter(self.__pk_name__)(self.__model__) == pk)
            .returning(self.__model__)
        )
        print(stmt)
        result = await self._session.scalars(stmt)
        return result.unique().one_or_none()

    async def delete_many_by_id(self, *pk: PrimaryKey) -> Iterable[TModel | None]:
        stmt = delete(self.__model__).where(
            attrgetter(self.__pk_name__)(self.__model__).in_(*pk)
        )
        result = await self._session.scalars(stmt)
        return result.unique().all()

    async def update(self, pk: PrimaryKey, **data: dict[str, Any]) -> TModel | None:
        stmt = (
            update(self.__model__)
            .where(attrgetter(self.__pk_name__)(self.__model__) == pk)
            .values(data)
            .returning(self.__model__)
        )
        result = await self._session.scalars(stmt)
        return result.unique().one_or_none()

    async def update_many(
        self, *entities: tuple[PrimaryKey, dict[str, Any]]
    ) -> Iterable[TModel | None]:
        stmt = update(self.__model__)
        r = []
        for entity in entities:
            q = (
                stmt.where(attrgetter(self.__pk_name__)(self.__model__) == entity[0])
                .values(*entity[1:])
                .returning(self.__model__)
            )
            r.append((await self._session.scalars(q)).unique().one_or_none())
        await self._session.commit()
        return r


class BankAsyncRepository(SQLAlchemyAsyncRepository[models.Bank]):
    __model__ = models.Bank

    async def get_by_name(self, name: str) -> models.Bank | None:
        stmt = select(self.__model__).where(self.__model__.name == name)
        return (await self._session.scalars(stmt)).unique().one_or_none()


class BankOfficeAsyncRepository(SQLAlchemyAsyncRepository[models.BankOffice]):
    __model__ = models.BankOffice


class BankAtmAsyncRepository(SQLAlchemyAsyncRepository[models.BankAtm]):
    __model__ = models.BankAtm


class EmployeeAsyncRepository(SQLAlchemyAsyncRepository[models.Employee]):
    __model__ = models.Employee


class CreditAccountAsyncRepository(SQLAlchemyAsyncRepository[models.CreditAccount]):
    __model__ = models.CreditAccount


class PaymentAccountAsyncRepository(SQLAlchemyAsyncRepository[models.PaymentAccount]):
    __model__ = models.PaymentAccount


class UserAsyncRepository(SQLAlchemyAsyncRepository[models.User]):
    __model__ = models.User
