from typing import Annotated, Iterable

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import selectinload
from starlette import status
from sqlalchemy import select

from src.models.banks import Bank, BankOffice, BankAtm
from src.routes.dependencies import get_bank_service, get_office_service
from src.routes.exceptions import BankNotFoundException, BankOfficeNotFoundException
from src.services.bank import BankService, BankOfficeService

bank_route = APIRouter(prefix="/bank", tags=["Bank"])


class CreateBankRequest(BaseModel):
    name: str


BankServiceDepends = Annotated[BankService, Depends(get_bank_service)]


@bank_route.put("/", status_code=status.HTTP_201_CREATED)
async def create_bank(
    service: BankServiceDepends,
    schema: CreateBankRequest,
):
    bank = Bank(name=schema.name)
    await service.create(bank)

    return CreateBankRequest(name=bank.name)


@bank_route.delete("/id/{id}", status_code=status.HTTP_200_OK)
async def delete_by_id(service: BankServiceDepends, id: int):
    if await service.delete_by_id(id) is None:
        raise BankNotFoundException()


@bank_route.get("/{id}", status_code=status.HTTP_200_OK)
async def get_bank_by_id(service: BankServiceDepends, id: int):
    result = await service.get_by_id(id)
    if result is None:
        raise BankNotFoundException()


@bank_route.get("/name/{name}", status_code=status.HTTP_200_OK)
async def get_bank_by_name(service: BankServiceDepends, name: str) -> Bank:
    result = await service.get_by_name(name)
    if result is None:
        raise BankNotFoundException()
    return result


@bank_route.get("/", status_code=status.HTTP_200_OK)
async def get_all_banks(service: BankServiceDepends) -> Iterable[Bank]:
    return await service.get_all()


office_route = APIRouter(prefix=f"{bank_route.prefix}/office", tags=["BankOffice"])

BankOfficeServiceDepends = Annotated[BankOfficeService, Depends(get_office_service)]


class BaseCreateBankOfficeRequest(BaseModel):
    name: str
    rental: int


class CreateBankOfficeWithOwnerRequest(BaseCreateBankOfficeRequest):
    owner: str | None = Field(default=None, title="Owner(bank name) of office")


@office_route.get("/{id}", status_code=status.HTTP_200_OK)
async def get_office_by_id(service: BankOfficeServiceDepends, pk: int) -> Bank | None:
    stmt = (
        select(BankOffice)
        .where(BankOffice.id == pk)
        .options(
            selectinload(BankOffice.bank),
        )
    )
    result = await service.session.scalar(stmt)
    # result = await service.get_by_id(id)
    if result is None:
        raise BankOfficeNotFoundException()
    return result.bank


@office_route.get("/", status_code=status.HTTP_200_OK)
async def get_all_offices(service: BankOfficeServiceDepends) -> Iterable[BankOffice]:
    result = await service.get_all()
    return result


@office_route.put("/", status_code=status.HTTP_201_CREATED)
async def create_office(
    office_service: BankOfficeServiceDepends,
    bank_service: BankServiceDepends,
    schema: CreateBankOfficeWithOwnerRequest,
):
    bank: Bank | None = None
    if schema.owner is not None:
        bank = await bank_service.get_by_name(schema.owner)
        if bank is None:
            raise BankNotFoundException()

    office = BankOffice(name=schema.name, rental=schema.rental, bank=bank)
    await office_service.create(office)
