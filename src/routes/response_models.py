from datetime import date

from pydantic import BaseModel, ConfigDict

from src.models.models import EmployeeStatus, BankAtmStatus, BankOfficeStatus


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
    users: list["User"]
    atms: list["BankAtm"]
    offices: list["BankOffice"]
    employees: list["Employee"]


class User(PersonModel):
    model_config = ConfigDict(from_attributes=True)
    work_place: str | None
    bank_credit_score: float
    monthly_income: float


class UserDetail(User):
    model_config = ConfigDict(from_attributes=True)
    banks: list["Bank"]
    credit_accounts: list["CreditAccount"]
    payment_accounts: list["PaymentAccount"]


class Employee(PersonModel):
    model_config = ConfigDict(from_attributes=True)
    position: str
    salary: int
    status: EmployeeStatus | None


class EmployeeDetail(Employee):
    model_config = ConfigDict(from_attributes=True)
    bank: "Bank | None"
    office: "BankOffice | None"


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
    user: User | None
    bank: Bank | None
    employee: Employee | None
    payment_account: "PaymentAccount | None"


class PaymentAccount(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    balance: int

    user_id: int
    bank_id: int


class PaymentAccountDetail(PaymentAccount):
    model_config = ConfigDict(from_attributes=True)
    user: "User| None"
    bank: "Bank| None"


class BankAtm(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    amortization: int
    status: BankAtmStatus | None


class BankAtmDetail(BankAtm):
    model_config = ConfigDict(from_attributes=True)
    office: "BankOffice | None"
    bank: "Bank | None"


class BankOffice(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    rental: int
    status: BankOfficeStatus | None


class BankOfficeDetail(BankOffice):
    model_config = ConfigDict(from_attributes=True)
    bank: "Bank | None"
    atms: list["BankAtm"]
