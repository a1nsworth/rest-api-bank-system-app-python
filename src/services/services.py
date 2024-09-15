from typing import Iterable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.base import Base
from src.models.models import Bank, User, BankOffice
from src.schemas import schemas as request_schemas


async def _update[TModel: Base](session: AsyncSession, model: TModel, **attrs):
    for key, value in attrs.items():
        if hasattr(model, key):
            setattr(session, key, value)


class BankService:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get(self, name: str) -> Bank | None:
        stmt = (
            select(Bank)
            .where(Bank.name == name)
            .options(
                selectinload(Bank.users),
                selectinload(Bank.offices),
                selectinload(Bank.atms),
                selectinload(Bank.employees),
            )
        )
        return (await self._session.execute(stmt)).scalar_one_or_none()

    async def get_many(self, *names: str) -> Iterable[Bank]:
        stmt = (
            select(Bank)
            .where(Bank.name.in_(names))
            .options(
                selectinload(Bank.users),
                selectinload(Bank.offices),
                selectinload(Bank.atms),
                selectinload(Bank.employees),
            )
        )
        return await self._session.scalars(stmt)

    async def all(self) -> Iterable[Bank]:
        return await self._session.scalars(
            select(Bank).options(
                selectinload(Bank.users),
                selectinload(Bank.offices),
                selectinload(Bank.atms),
                selectinload(Bank.employees),
            )
        )

    async def create(self, schema: request_schemas.BankCreate):
        found = await self.get(schema.name)
        if found:
            return

        self._session.add(Bank(name=schema.name))
        await self._session.commit()

    async def delete(self, name: str) -> Bank | None:
        found = await self.get(name)
        if not found:
            return None
        await self._session.delete(found)
        await self._session.commit()
        return found

    async def update(self, schema: request_schemas.BankUpdate) -> Bank | None:
        found = await self.get(schema.name)
        if not found:
            return
        found.name = schema.new_name
        await self._session.commit()
        return found


class UserService:
    def __init__(self, session: AsyncSession, bank_service: BankService):
        self._session = session
        self._bank_service = bank_service

    async def get(self, pk: int) -> User | None:
        stmt = (
            select(User)
            .where(User.id == pk)
            .options(
                selectinload(User.banks),
                selectinload(User.payment_accounts),
                selectinload(User.credit_accounts),
            )
        )
        return (await self._session.execute(stmt)).scalar_one_or_none()

    async def all(self) -> Iterable[User]:
        return await self._session.scalars(
            select(User).options(
                selectinload(User.banks),
                selectinload(User.payment_accounts),
                selectinload(User.credit_accounts),
            )
        )

    async def create(self, schema: request_schemas.UserCreate):
        self._session.add(User(**schema.model_dump()))
        await self._session.commit()

    async def delete(self, pk: int) -> User | None:
        found = await self.get(pk)
        if not found:
            return
        await self._session.delete(found)
        await self._session.commit()
        return found

    async def update(self, pk: int, **attrs) -> User | None:
        found = await self.get(pk)
        if not found:
            return
        await _update(self._session, found, **attrs)
        await self._session.commit()
        return found

    async def connect_banks(self, schema: request_schemas.ConnectUserToBanks):
        banks = list(await self._bank_service.get_many(*schema.names))
        if len(banks) != len(schema.names):
            raise ValueError("not all bank exist")

        user = await self.get(schema.id)
        if user is None:
            raise ValueError("user not found")

        user.banks.extend(banks)
        await self._session.commit()


class BankOfficeService:
    def __init__(self, session: AsyncSession, bank_service: BankService):
        self._session = session
        self._bank_service = bank_service

    async def get(self, pk: int) -> BankOffice | None:
        stmt = (
            select(BankOffice)
            .where(BankOffice.id == pk)
            .options(
                selectinload(BankOffice.bank),
                selectinload(BankOffice.atms),
            )
        )
        return (await self._session.execute(stmt)).scalar_one_or_none()

    async def all(self) -> Iterable[BankOffice]:
        return await self._session.scalars(
            select(BankOffice).options(
                selectinload(BankOffice.bank),
                selectinload(BankOffice.atms),
            )
        )

    async def create(self, schema: request_schemas.BankOfficeCreate):
        owner = await self._bank_service.get(schema.owner)
        if owner is None:
            raise ValueError("Owner not found")
        self._session.add(
            BankOffice(bank=owner, name=schema.name, rental=schema.rental)
        )
        await self._session.commit()

    async def delete(self, pk: int) -> BankOffice | None:
        found = await self.get(pk)
        if not found:
            return
        await self._session.delete(found)
        await self._session.commit()
        return found

    async def update(self, pk: int, **attrs) -> BankOffice | None:
        found = await self.get(pk)
        if not found:
            return
        await _update(self._session, found, **attrs)
        await self._session.commit()
        return found
