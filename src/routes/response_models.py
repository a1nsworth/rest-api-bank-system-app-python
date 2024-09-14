from pydantic import BaseModel, ConfigDict
from datetime import date

from src.models.banks import EmployeeStatus, BankAtmStatus, BankOfficeStatus


class PersonModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    first_name: str
    second_name: str
    patronymic_name: str | None


class Bank(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    rating: int
    total_sum: int


class BankDetail(Bank):
    model_config = ConfigDict(from_attributes=True)
    atms: list["BankAtmDetail"]
    offices: list["BankOfficeDetail"]
    employees: list["EmployeeDetail"]


class User(PersonModel):
    model_config = ConfigDict(from_attributes=True)
    work_place: str | None
    bank_credit_score: float
    mouthly_income: float


class UserDetail(User):
    model_config = ConfigDict(from_attributes=True)
    credit_accounts: list["CreditAccountDetail"]
    payment_accounts: list["PaymentAccountDetail"]


class Employee(PersonModel):
    model_config = ConfigDict(from_attributes=True)
    position: str
    salary: int
    status: EmployeeStatus | None


class EmployeeDetail(Employee):
    model_config = ConfigDict(from_attributes=True)
    bank: "BankDetail | None"
    office: "BankOfficeDetail | None"


class CreditAccount(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    loan_start_date: date
    loan_end_date: date
    load_duration_mounts: int
    loan_amount: int
    mounthly_payment: int
    interest_rate: int


class CreditAccountDetail(CreditAccount):
    model_config = ConfigDict(from_attributes=True)
    user: "UserDetail | None"
    bank: "BankDetail | None"
    employee: "EmployeeDetail | None"
    payment_account: "PaymentAccountDetail | None"


class PaymentAccount(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    balance: int


class PaymentAccountDetail(PaymentAccount):
    model_config = ConfigDict(from_attributes=True)
    user: "UserDetail | None"
    bank: "BankDetail | None"


class BankAtm(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    amortization: int
    status: BankAtmStatus | None


class BankAtmDetail(BankAtm):
    model_config = ConfigDict(from_attributes=True)
    office: "BankOfficeDetail | None"
    bank: "BankDetail | None"


class BankOffice(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    rental: int
    status: BankOfficeStatus | None


class BankOfficeDetail(BankOffice):
    model_config = ConfigDict(from_attributes=True)
    bank: "BankDetail | None"
    atms: list["BankAtmDetail"]
