from dataclasses import dataclass, field
from enum import Flag, auto
from datetime import date

import pypika


@dataclass(frozen=True, slots=True)
class WithPrimalKey:
    id: int | None = field(kw_only=True)


@dataclass(frozen=True, slots=True)
class PersonModel:
    first_name: str
    second_name: str
    patronymic_name: str | None
    date_of_birth: date


@dataclass(frozen=True, slots=True)
class BankUser:
    user_id: int
    bank_id: int


@dataclass(frozen=True, slots=True)
class Bank(WithPrimalKey):
    name: str
    rating: int = field(init=False)
    total_sum: int = field(init=False)

    atms: list["BankAtm"] = field(default_factory=list, init=False)
    offices: list["BankOffice"] = field(default_factory=list, init=False)
    employees: list["Employee"] = field(default_factory=list, init=False)
    users: list["User"] = field(default_factory=list, init=False)


@dataclass(frozen=True, slots=True)
class User(WithPrimalKey, PersonModel):
    work_place: str | None
    bank_credit_score: int
    mouthly_income: float = field(init=False)

    banks: list["Bank"] = field(default_factory=list)
    credit_accounts: list["CreditAccount"] = field(default_factory=list)
    payment_accounts: list["PaymentAccount"] = field(default_factory=list)


class EmployeeStatus(Flag):
    IsRemote = auto()
    CanGiveLoans = auto()


@dataclass(frozen=True, slots=True)
class Employee(WithPrimalKey, PersonModel):
    position: str
    salary: int

    bank_id: int | None = field(default=None, init=False)
    bank: "Bank | None" = field(default=None, kw_only=True)
    office_id: int | None = field(default=None, init=False)
    offices: "BankOffice | None" = field(kw_only=True)
    status: EmployeeStatus | None = None


@dataclass(frozen=True, slots=True)
class CreditAccount(WithPrimalKey, PersonModel):
    loan_start_date: date
    loan_end_date: date
    load_duration_mounts: int
    loan_amount: int
    mouthly_payment: int
    interest_rate: int

    user_id: int | None = field(default=None, init=False)
    user: "User | None" = field(default=None, kw_only=True)
    bank_id: int | None = field(default=None, init=False)
    bank: "Bank | None" = field(default=None, kw_only=True)
    employee_id: int | None = field(default=None, init=False)
    employee: "Employee | None" = field(default=None, kw_only=True)
    payment_account_id: int | None = field(default=None, init=False)
    payment_account: "PaymentAccount | None" = field(default=None, kw_only=True)


@dataclass(frozen=True, slots=True)
class PaymentAccount(WithPrimalKey):
    balance: int

    user_id: int | None = field(default=None, init=False)
    user: "User | None" = field(default=None, kw_only=True)
    bank_id: int | None = field(default=None, init=False)
    bank: "Bank | None" = field(default=None, kw_only=True)


class BankAtmStatus(Flag):
    Active = auto()
    HaveMoney = auto()
    WorkToDespenseMoney = auto()
    AbleWithdraw = auto()


class BankAtm(WithPrimalKey):
    name: str
    amortization: int
    status: BankAtmStatus | None = field(default=None)

    bank_id: int | None = field(default=None, init=False)
    bank: "Bank | None" = field(default=None, kw_only=True)
    office_id: int | None = field(default=None, init=False)
    offices: "BankOffice | None" = field(default=None, kw_only=True)


class BankOfficeStatus(Flag):
    Active = auto()
    AbleToPlaceAtm = auto()
    CreditAvailable = auto()


class BankOffice(WithPrimalKey):
    name: str
    rental: int
    status: BankOfficeStatus | None = field(default=None)

    bank_id: int | None = field(default=None, init=False)
    bank: "Bank | None" = field(default=None, kw_only=True)
    atms: list["BankAtm"] = field(default_factory=list, kw_only=True)
