from typing import Iterable, Any

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, HTTPException
from starlette import status

from src.routes.exceptions import (
    BankNotFoundException,
    BankOfficeNotFoundException,
    UserNotFoundException,
)
from src.routes.response_models import BankDetail, BankOfficeDetail, UserDetail
from src.schemas import schemas as request_schemas
from src.services.services import BankService, BankOfficeService, UserService

bank_route = APIRouter(prefix="/bank", tags=["Bank"], route_class=DishkaRoute)


@bank_route.put("/", status_code=status.HTTP_201_CREATED)
async def create_bank(
    service: FromDishka[BankService],
    schema: request_schemas.BankCreate,
):
    try:
        await service.create(schema)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@bank_route.get(
    "/name/{name}", response_model=BankDetail, status_code=status.HTTP_200_OK
)
async def get_bank_by_name(service: FromDishka[BankService], name: str) -> Any:
    result = await service.get(name)
    if result is None:
        raise BankNotFoundException()
    return result


@bank_route.get(
    "/", response_model=Iterable[BankDetail], status_code=status.HTTP_200_OK
)
async def get_all_banks(service: FromDishka[BankService]) -> Any:
    return await service.all()


@bank_route.patch("/", status_code=status.HTTP_200_OK)
async def update_bank(
    services: FromDishka[BankService], schema: request_schemas.BankUpdate
):
    await services.update(schema)


@bank_route.delete(
    "/name/{name}", response_model=BankDetail | None, status_code=status.HTTP_200_OK
)
async def delete_bank(services: FromDishka[BankService], name: str):
    result = await services.delete(name)
    if result is None:
        raise BankNotFoundException()
    return result


office_route = APIRouter(
    prefix=f"{bank_route.prefix}/office", tags=["BankOffice"], route_class=DishkaRoute
)


@office_route.get(
    "/{id}", response_model=BankOfficeDetail, status_code=status.HTTP_200_OK
)
async def get_office_by_id(service: FromDishka[BankOfficeService], pk: int):
    result = await service.get(pk)
    if result is None:
        raise BankOfficeNotFoundException()
    return result


@office_route.get(
    "/", response_model=Iterable[BankOfficeDetail], status_code=status.HTTP_200_OK
)
async def get_all_offices(
    service: FromDishka[BankOfficeService],
):
    return await service.all()


@office_route.put("/", status_code=status.HTTP_201_CREATED)
async def create_office(
    office_service: FromDishka[BankOfficeService],
    schema: request_schemas.BankOfficeCreate,
):
    try:
        await office_service.create(schema)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@office_route.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_office_by_id(service: FromDishka[BankOfficeService], pk: int):
    result = await service.delete(pk)
    if result is None:
        raise BankNotFoundException()


user_route = APIRouter(prefix="/user", tags=["User"], route_class=DishkaRoute)


@user_route.get("/{id}", response_model=UserDetail, status_code=status.HTTP_200_OK)
async def get_user_by_id(service: FromDishka[UserService], pk: int):
    result = await service.get(pk)
    if result is None:
        raise UserNotFoundException()
    return result


@user_route.get(
    "/", response_model=Iterable[UserDetail], status_code=status.HTTP_200_OK
)
async def get_all_users(service: FromDishka[UserService]):
    return await service.all()


@user_route.put("/", status_code=status.HTTP_201_CREATED)
async def create_user(
    service: FromDishka[UserService], schema: request_schemas.UserCreate
):
    await service.create(schema)


@user_route.delete("/", response_model=UserDetail, status_code=status.HTTP_200_OK)
async def delete_user(service: FromDishka[UserService], pk: int):
    result = await service.delete(pk)
    if result is None:
        raise UserNotFoundException()
    return result


@user_route.patch("/", status_code=status.HTTP_200_OK)
async def connect_user_to_bank(
    service: FromDishka[UserService], schema: request_schemas.ConnectUserToBanks
):
    try:
        await service.connect_banks(schema)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
