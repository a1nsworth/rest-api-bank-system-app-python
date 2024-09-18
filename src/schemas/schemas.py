from datetime import date

from pydantic import BaseModel
from pydantic.fields import Field

from src.models.models import BankOfficeStatus, BankAtmStatus


class PersonModel(BaseModel):
    first_name: str
    second_name: str
    patronymic_name: str | None
    date_of_birth: date


class PersonalModelPartialUpdate(BaseModel):
    first_name: str | None = None
    second_name: str | None = None
    patronymic_name: str | None = None


class BankCreate(BaseModel):
    name: str


class BankUpdateByName(BaseModel):
    name: str
    new_name: str


class BankUpdateById(BaseModel):
    id: int
    new_name: str


class UserCreate(PersonModel):
    work_place: str | None


class UserPartialUpdate(PersonalModelPartialUpdate):
    id: int
    work_place: str | None = None


class BankOfficeCreate(BaseModel):
    name: str
    rental: int
    status: BankOfficeStatus | None = None


class BankOfficeUpdate(BaseModel):
    id: int
    name: str | None = Field(default=None, examples=[None])
    rental: int | None = Field(default=None, examples=[None])
    status: BankOfficeStatus | None = Field(default=None, examples=[None])


class EmployeeCreate(PersonModel):
    position: str
    salary: int


class EmployeePartialUpdate(PersonalModelPartialUpdate):
    id: int
    position: str | None = None
    salary: int | None = None


class CreditAccountCreate(BaseModel):
    loan_start_date: date
    loan_end_date: date
    load_duration_mounts: int
    loan_amount: int
    mounthly_payment: int
    interest_rate: int

    user_id: int
    bank_id: int
    payment_account_id: int
    employee_id: int


class CreditAccountPartialUpdate(BaseModel):
    id: int

    loan_start_date: date | None = None
    loan_end_date: date | None = None
    load_duration_mounts: int | None = None
    loan_amount: int | None = None
    mounthly_payment: int | None = None
    interest_rate: int | None = None


class PaymentAccountCreate(BaseModel):
    balance: int

    user_id: int
    bank_id: int


class PaymentAccountPartialUpdate(BaseModel):
    balance: int | None = None


class BankAtmCreate(BaseModel):
    name: str
    amortization: int
    status: BankAtmStatus | None = None

    office_id: int
    bank_id: int


class BankAtmPartialUpdate(BaseModel):
    name: str | None = None
    amortization: int | None = None
    status: BankAtmStatus | None = None

    office_id: int | None = None
    bank_id: int | None = None
