from functools import cached_property
from typing import Any, Iterable

from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService
from sqlalchemy.orm import selectinload
from sqlalchemy.orm.strategy_options import _AbstractLoad

from src.models import models
from src.repositories import repositories
from src.schemas import schemas as request_schemas
from src.services import exceptions


class BankService(SQLAlchemyAsyncRepositoryService[models.Bank]):  # type: ignore
    repository_type = repositories.BankRepository

    @cached_property
    def _all_loads(self) -> tuple[_AbstractLoad, ...]:
        return (
            selectinload(models.Bank.users),
            selectinload(models.Bank.employees),
            selectinload(models.Bank.offices),
            selectinload(models.Bank.atms),
        )

    async def get_by_id(self, pk) -> models.Bank:
        return await super().get(pk, load=self._all_loads)

    async def get_by_name(self, name: str) -> models.Bank:
        return await self.get_one(
            models.Bank.name == name,
            load=self._all_loads,
        )

    async def list(self) -> Iterable[models.Bank]:
        return await super().list(load=self._all_loads)

    async def create(self, schema: request_schemas.BankCreate) -> models.Bank:
        found = await self.exists(models.Bank.name == schema.name)
        if found:
            raise exceptions.AlreadyExistsError(
                f"bank with {schema.name=} already exists"
            )
        return await super().create(schema.model_dump(), auto_commit=True)

    async def delete_by_id(self, pk) -> models.Bank:
        return await super().delete(pk, load=self._all_loads, auto_commit=True)

    async def delete_by_name(self, name: str) -> models.Bank:
        bank = await self.get_by_name(name)
        await self.repository.session.delete(bank)
        await self.repository.session.commit()
        return bank

    async def update_by_id(self, schema: request_schemas.BankUpdateById) -> models.Bank:
        return await super().update(
            {"name": schema.new_name},
            schema.id,
            auto_commit=True,
        )

    async def update_by_name(
        self, schema: request_schemas.BankUpdateByName
    ) -> models.Bank:
        bank = await self.get_by_name(schema.name)
        bank.name = schema.new_name
        await self.repository.session.commit()
        return bank


class BankOfficeService(SQLAlchemyAsyncRepositoryService[models.BankOffice]):  # type: ignore
    repository_type = repositories.BankOfficeRepository

    async def partial_update(self, pk, **attrs) -> models.BankOffice:
        bank_office = await self.get(pk, load="*")
        for k, v in attrs.items():
            if hasattr(bank_office, k):
                setattr(bank_office, k, v)
        await self.repository.session.commit()
        return bank_office


class UserService(SQLAlchemyAsyncRepositoryService[models.User]):  # type: ignore
    repository_type = repositories.UserRepository

    async def partial_update(self, pk: Any, **attrs) -> models.User:
        user = await self.get(pk, load="*")
        for k, v in attrs.items():
            if hasattr(user, k):
                setattr(user, k, v)
        await self.repository.session.commit()
        return user


class EmployeeService(SQLAlchemyAsyncRepositoryService[models.Employee]):  # type: ignore
    repository_type = repositories.EmployeeRepository

    async def partial_update(self, pk: Any, **attrs) -> models.Employee:
        employee = await self.get(pk, load="*")
        for k, v in attrs.items():
            if hasattr(employee, k):
                setattr(employee, k, v)
        await self.repository.session.commit()
        return employee


class CreditAccountService(SQLAlchemyAsyncRepositoryService[models.CreditAccount]):  # type: ignore
    repository_type = repositories.CreditAccountRepository

    @cached_property
    def _all_loads(self) -> tuple[_AbstractLoad, ...]:
        return (
            selectinload(models.CreditAccount.payment_account),
            selectinload(models.CreditAccount.bank),
            selectinload(models.CreditAccount.employee),
            selectinload(models.CreditAccount.user),
        )

    async def list(self) -> Iterable[models.CreditAccount]:
        return await super().list(load=self._all_loads)

    async def partial_update(self, pk: Any, **attrs) -> models.CreditAccount:
        m = await self.get(pk, load="*")
        for k, v in attrs.items():
            if hasattr(m, k):
                setattr(m, k, v)
        await self.repository.session.commit()
        return m


class PaymentAccountService(SQLAlchemyAsyncRepositoryService[models.PaymentAccount]):  # type: ignore
    repository_type = repositories.PaymentAccountRepository

    async def partial_update(self, pk: Any, **attrs) -> models.PaymentAccount:
        m = await self.get(pk, load="*")
        for k, v in attrs.items():
            if hasattr(m, k):
                setattr(m, k, v)
        await self.repository.session.commit()
        return m


class BankAtmService(SQLAlchemyAsyncRepositoryService[models.BankAtm]):  # type: ignore
    repository_type = repositories.BankAtmRepository

    async def partial_update(self, pk: Any, **attrs) -> models.BankAtm:
        m = await self.get(pk, load="*")
        for k, v in attrs.items():
            if hasattr(m, k):
                setattr(m, k, v)
        await self.repository.session.commit()
        return m
