from typing import Iterable

from advanced_alchemy.exceptions import NotFoundError
from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, HTTPException
from starlette import status

from src.routes import response_models
from src.schemas import schemas as request_schemas
from src.services import exceptions as services_exceptions
from src.services import services

bank_route = APIRouter(prefix="/bank", tags=["Bank"], route_class=DishkaRoute)


@bank_route.get(
    "/",
    response_model=Iterable[response_models.BankDetail],
    status_code=status.HTTP_200_OK,
)
async def get_all_banks(service: FromDishka[services.BankService]):
    return await service.list()


@bank_route.get(
    "/{id}", response_model=response_models.BankDetail, status_code=status.HTTP_200_OK
)
async def get_bank_by_id(service: FromDishka[services.BankService], pk: int):
    try:
        return await service.get_by_id(pk)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@bank_route.get(
    "/name/{name}",
    response_model=response_models.BankDetail,
    status_code=status.HTTP_200_OK,
)
async def get_bank_by_name(service: FromDishka[services.BankService], name: str):
    try:
        return await service.get_by_name(name)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@bank_route.put(
    "/", response_model=response_models.Bank, status_code=status.HTTP_201_CREATED
)
async def create_bank(
    service: FromDishka[services.BankService], schema: request_schemas.BankCreate
):
    try:
        return await service.create(schema)
    except services_exceptions.AlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@bank_route.delete(
    "/{pk}", response_model=response_models.BankDetail, status_code=status.HTTP_200_OK
)
async def delete_bank_by_id(service: FromDishka[services.BankService], pk: int):
    try:
        return await service.delete_by_id(pk)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@bank_route.delete(
    "/name/{name}",
    response_model=response_models.BankDetail,
    status_code=status.HTTP_200_OK,
)
async def delete_bank_by_name(service: FromDishka[services.BankService], name: str):
    try:
        return await service.delete_by_name(name)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@bank_route.patch(
    "/", response_model=response_models.BankDetail, status_code=status.HTTP_200_OK
)
async def update_bank_by_name(
    service: FromDishka[services.BankService], schema: request_schemas.BankUpdateByName
):
    try:
        return await service.update_by_name(schema)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


bank_office_route = APIRouter(
    prefix="/bank/office", tags=["BankOffice"], route_class=DishkaRoute
)


@bank_office_route.get(
    "/",
    response_model=Iterable[response_models.BankOfficeDetail],
    status_code=status.HTTP_200_OK,
)
async def get_all_offices(service: FromDishka[services.BankOfficeService]):
    return await service.list(load="*")


@bank_office_route.get(
    "/{pk}",
    response_model=response_models.BankOfficeDetail,
    status_code=status.HTTP_200_OK,
)
async def get_by_office_id(service: FromDishka[services.BankOfficeService], pk: int):
    try:
        return await service.get(pk, load="*")
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@bank_office_route.put(
    "/",
    response_model=response_models.BankOffice,
    status_code=status.HTTP_201_CREATED,
)
async def create_office(
    service: FromDishka[services.BankOfficeService],
    schema: request_schemas.BankOfficeCreate,
):
    return await service.create(schema.model_dump(), auto_commit=True)


@bank_office_route.delete(
    "/{pk}",
    response_model=response_models.BankOfficeDetail,
    status_code=status.HTTP_200_OK,
)
async def delete_office_by_id(service: FromDishka[services.BankOfficeService], pk: int):
    try:
        return await service.delete(pk, load="*", auto_commit=True)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@bank_office_route.patch(
    "/",
    response_model=response_models.BankOfficeDetail,
    status_code=status.HTTP_200_OK,
)
async def update_office(
    service: FromDishka[services.BankOfficeService],
    schema: request_schemas.BankOfficeUpdate,
):
    try:
        return await service.partial_update(
            schema.id, **schema.model_dump(exclude={"id"}, exclude_none=True)
        )
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


bank_atm_route = APIRouter(
    prefix="/bank/atm", tags=["Bank Atm"], route_class=DishkaRoute
)


@bank_atm_route.get(
    "/",
    response_model=Iterable[response_models.BankAtmDetail],
    status_code=status.HTTP_200_OK,
)
async def get_all_bank_atms(service: FromDishka[services.BankAtmService]):
    return await service.list(load="*")


@bank_atm_route.get(
    "/{pk}",
    response_model=response_models.BankAtmDetail,
    status_code=status.HTTP_200_OK,
)
async def get_bank_atm_by_id(service: FromDishka[services.BankAtmService], pk: int):
    try:
        return await service.get(pk, load="*")
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@bank_atm_route.put(
    "/",
    response_model=response_models.BankAtm,
    status_code=status.HTTP_201_CREATED,
)
async def create_bank_atm(
    service: FromDishka[services.BankAtmService],
    schema: request_schemas.BankAtmCreate,
):
    return await service.create(schema.model_dump(), auto_commit=True)


@bank_atm_route.delete(
    "/{pk}",
    response_model=response_models.BankAtmDetail,
    status_code=status.HTTP_200_OK,
)
async def bank_atm_by_id(service: FromDishka[services.BankAtmService], pk: int):
    try:
        return await service.delete(pk, load="*", auto_commit=True)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@bank_atm_route.patch(
    "/",
    response_model=response_models.BankAtmDetail,
    status_code=status.HTTP_200_OK,
)
async def update_bank_atm(
    service: FromDishka[services.BankAtmService],
    schema: request_schemas.BankOfficeUpdate,
):
    try:
        return await service.partial_update(
            schema.id, **schema.model_dump(exclude={"id"}, exclude_none=True)
        )
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


user_route = APIRouter(prefix="/user", tags=["User"], route_class=DishkaRoute)


@user_route.get(
    "/",
    response_model=Iterable[response_models.UserDetail],
    status_code=status.HTTP_200_OK,
)
async def get_all_users(service: FromDishka[services.UserService]):
    return await service.list(load="*")


@user_route.get(
    "/{id}", response_model=response_models.UserDetail, status_code=status.HTTP_200_OK
)
async def get_user_by_id(service: FromDishka[services.UserService], pk: int):
    try:
        return await service.get(pk, load="*")
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@user_route.put(
    "/", response_model=response_models.User, status_code=status.HTTP_201_CREATED
)
async def create_user(
    service: FromDishka[services.UserService], schema: request_schemas.UserCreate
):
    return await service.create(schema.model_dump(), auto_commit=True)


@user_route.delete(
    "/{id}", response_model=response_models.UserDetail, status_code=status.HTTP_200_OK
)
async def delete_user_by_id(service: FromDishka[services.UserService], pk: int):
    try:
        return await service.delete(pk, load="*", auto_commit=True)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@user_route.patch(
    "/", response_model=response_models.User, status_code=status.HTTP_200_OK
)
async def update_user(
    service: FromDishka[services.UserService], schema: request_schemas.UserPartialUpdate
):
    try:
        return await service.partial_update(
            schema.id, **schema.model_dump(exclude={"id"}, exclude_none=True)
        )
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


employee_route = APIRouter(
    prefix="/employee", tags=["Employee"], route_class=DishkaRoute
)


@employee_route.get(
    "/",
    response_model=Iterable[response_models.EmployeeDetail],
    status_code=status.HTTP_200_OK,
)
async def get_all_employees(service: FromDishka[services.EmployeeService]):
    return await service.list(load="*")


@employee_route.get(
    "/{id}",
    response_model=response_models.EmployeeDetail,
    status_code=status.HTTP_200_OK,
)
async def get_employee_by_id(service: FromDishka[services.EmployeeService], pk: int):
    try:
        return await service.get(pk, load="*")
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@employee_route.put(
    "/", response_model=response_models.Employee, status_code=status.HTTP_201_CREATED
)
async def create_employee(
    service: FromDishka[services.EmployeeService],
    schema: request_schemas.EmployeeCreate,
):
    return await service.create(schema.model_dump(), auto_commit=True)


@employee_route.delete(
    "/{id}",
    response_model=response_models.EmployeeDetail,
    status_code=status.HTTP_200_OK,
)
async def delete_employee_by_id(service: FromDishka[services.EmployeeService], pk: int):
    try:
        return await service.get(pk, load="*")
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@employee_route.patch(
    "/", response_model=response_models.Employee, status_code=status.HTTP_200_OK
)
async def update_employee(
    service: FromDishka[services.EmployeeService],
    schema: request_schemas.EmployeePartialUpdate,
):
    try:
        return await service.partial_update(
            schema.id, **schema.model_dump(exclude={"id"}, exclude_none=True)
        )
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


credit_account_route = APIRouter(
    prefix="/bank/credit/account", tags=["Credit Account"], route_class=DishkaRoute
)


@credit_account_route.get(
    "/",
    response_model=Iterable[response_models.CreditAccountDetail],
    status_code=status.HTTP_200_OK,
)
async def get_all_credit_accounts(service: FromDishka[services.CreditAccountService]):
    return await service.list()


@credit_account_route.get(
    "/{id}",
    response_model=response_models.CreditAccountDetail,
    status_code=status.HTTP_200_OK,
)
async def get_credit_account_by_id(
    service: FromDishka[services.CreditAccountService], pk: int
):
    try:
        return await service.get(pk, load="*")
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@credit_account_route.put(
    "/",
    response_model=response_models.CreditAccount,
    status_code=status.HTTP_201_CREATED,
)
async def create_credit_account(
    service: FromDishka[services.CreditAccountService],
    schema: request_schemas.CreditAccountCreate,
):
    return await service.create(schema.model_dump(), auto_commit=True)


@credit_account_route.delete(
    "/{id}",
    response_model=response_models.CreditAccountDetail,
    status_code=status.HTTP_200_OK,
)
async def delete_credit_account_by_id(
    service: FromDishka[services.CreditAccountService], pk: int
):
    try:
        return await service.get(pk, load="*")
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@credit_account_route.patch(
    "/", response_model=response_models.CreditAccount, status_code=status.HTTP_200_OK
)
async def update_credit_account(
    service: FromDishka[services.CreditAccountService],
    schema: request_schemas.CreditAccountPartialUpdate,
):
    try:
        return await service.partial_update(
            schema.id, **schema.model_dump(exclude={"id"}, exclude_none=True)
        )
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


payment_account_route = APIRouter(
    prefix="/bank/payment/account", tags=["Payment Account"], route_class=DishkaRoute
)


@payment_account_route.get(
    "/",
    response_model=Iterable[response_models.PaymentAccountDetail],
    status_code=status.HTTP_200_OK,
)
async def get_all_credit_accounts(service: FromDishka[services.PaymentAccountService]):
    return await service.list(load="*")


@payment_account_route.get(
    "/{id}",
    response_model=response_models.PaymentAccountDetail,
    status_code=status.HTTP_200_OK,
)
async def get_credit_account_by_id(
    service: FromDishka[services.PaymentAccountService], pk: int
):
    try:
        return await service.get(pk, load="*")
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@payment_account_route.put(
    "/",
    response_model=response_models.PaymentAccount,
    status_code=status.HTTP_201_CREATED,
)
async def create_payment_account(
    service: FromDishka[services.PaymentAccountService],
    schema: request_schemas.PaymentAccountCreate,
):
    return await service.create(schema.model_dump(), auto_commit=True)


@payment_account_route.delete(
    "/{id}",
    response_model=response_models.PaymentAccountDetail,
    status_code=status.HTTP_200_OK,
)
async def delete_payment_account_by_id(
    service: FromDishka[services.PaymentAccountService], pk: int
):
    try:
        return await service.get(pk, load="*")
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@payment_account_route.patch(
    "/", response_model=response_models.PaymentAccount, status_code=status.HTTP_200_OK
)
async def update_payment_account(
    service: FromDishka[services.CreditAccountService],
    schema: request_schemas.CreditAccountPartialUpdate,
):
    try:
        return await service.partial_update(
            schema.id, **schema.model_dump(exclude={"id"}, exclude_none=True)
        )
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
