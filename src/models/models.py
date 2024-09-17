import random
from enum import Flag, auto

from sqlalchemy import (
    String,
    ForeignKey,
    Enum,
    Date,
    PrimaryKeyConstraint,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from src.models.base import WithPK, PersonModel, Base


class BankUser(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    bank_id: Mapped[int] = mapped_column(ForeignKey("bank.id"))

    __table_args__ = (PrimaryKeyConstraint("user_id", "bank_id"),)


class Bank(WithPK):
    name: Mapped[str] = mapped_column(String(100), unique=True)
    rating: Mapped[int] = mapped_column(
        default_factory=lambda: random.randint(0, 100), init=False
    )
    total_sum: Mapped[int] = mapped_column(
        default_factory=lambda: random.randint(0, int(1e6)), init=False
    )
    users: Mapped[list["User"]] = relationship(
        back_populates="banks",
        default_factory=list,
        secondary="bank_user",
    )

    atms: Mapped[list["BankAtm"]] = relationship(
        back_populates="bank", default_factory=list
    )
    offices: Mapped[list["BankOffice"]] = relationship(
        back_populates="bank", default_factory=list
    )
    employees: Mapped[list["Employee"]] = relationship(
        back_populates="bank", default_factory=list
    )

    def count_atms(self) -> int:
        return len(self.atms)

    def count_offices(self) -> int:
        return len(self.offices)

    def count_clients(self) -> int:
        return len(self.offices)


class User(WithPK, PersonModel):
    work_place: Mapped[str | None] = mapped_column(String(100))
    bank_credit_score: Mapped[int] = mapped_column(
        default_factory=lambda: random.randint(0, 100), init=False
    )
    monthly_income: Mapped[float] = mapped_column(
        default_factory=lambda: round(random.uniform(0.0, 10000), 2), init=False
    )

    banks: Mapped[list["Bank"]] = relationship(
        back_populates="users",
        secondary="bank_user",
        default_factory=list,
    )

    credit_accounts: Mapped[list["CreditAccount"]] = relationship(
        back_populates="user", default_factory=list
    )
    payment_accounts: Mapped[list["PaymentAccount"]] = relationship(
        back_populates="user", default_factory=list
    )


class EmployeeStatus(Flag):
    IsRemote = auto()
    CanGiveLoans = auto()


class Employee(WithPK, PersonModel):
    position: Mapped[str] = mapped_column(String(30))
    salary: Mapped[int]

    bank_id: Mapped[int | None] = mapped_column(
        ForeignKey("bank.id", ondelete="CASCADE"), init=False
    )
    office_id: Mapped[int | None] = mapped_column(
        ForeignKey("bank_office.id", ondelete="SET NULL"), init=False
    )
    bank: Mapped["Bank | None"] = relationship(back_populates="employees", default=None)
    office: Mapped["BankOffice | None"] = relationship(default=None)
    status: Mapped[EmployeeStatus | None] = mapped_column(
        Enum(EmployeeStatus), default=None
    )


class CreditAccount(WithPK):
    loan_start_date = mapped_column(Date)
    loan_end_date = mapped_column(Date)
    load_duration_mounts: Mapped[int]
    loan_amount: Mapped[int]
    mounthly_payment: Mapped[int]
    interest_rate: Mapped[int]

    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"), init=False
    )
    bank_id: Mapped[int | None] = mapped_column(
        ForeignKey("bank.id", ondelete="CASCADE"), init=False
    )
    employee_id: Mapped[int | None] = mapped_column(
        ForeignKey("employee.id"), init=False
    )
    payment_account_id: Mapped[int | None] = mapped_column(
        ForeignKey("payment_account.id"), init=False
    )
    user: Mapped["User | None"] = relationship(
        back_populates="credit_accounts", default=None
    )
    bank: Mapped["Bank | None"] = relationship(default=None)
    employee: Mapped["Employee | None"] = relationship(default=None)
    payment_account: Mapped["PaymentAccount | None"] = relationship(default=None)


class PaymentAccount(WithPK):
    balance: Mapped[int]

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    bank_id: Mapped[int] = mapped_column(ForeignKey("bank.id", ondelete="CASCADE"))
    user: Mapped["User | None"] = relationship(
        back_populates="payment_accounts", default=None
    )
    bank: Mapped["Bank | None"] = relationship(default=None)


class BankAtmStatus(Flag):
    Active = auto()
    HaveMoney = auto()
    WorkToDespenseMoney = auto()
    AbleWithdraw = auto()


class BankAtm(WithPK):
    name: Mapped[str] = mapped_column(String(50))
    amortization: Mapped[int]

    bank_id: Mapped[int | None] = mapped_column(
        ForeignKey("bank.id", ondelete="CASCADE"), init=False
    )
    office_id: Mapped[int] = mapped_column(
        ForeignKey("bank_office.id", ondelete="CASCADE"), init=False
    )
    office: Mapped["BankOffice | None"] = relationship(
        back_populates="atms", default=None
    )
    bank: Mapped["Bank | None"] = relationship(back_populates="atms", default=None)

    status: Mapped[BankAtmStatus | None] = mapped_column(
        Enum(BankAtmStatus), default=None
    )


class BankOfficeStatus(Flag):
    Active = auto()
    AbleToPlaceAtm = auto()
    CreditAvailable = auto()


class BankOffice(WithPK):
    name: Mapped[str] = mapped_column(String(100))
    rental: Mapped[int]

    bank_id: Mapped[int | None] = mapped_column(
        ForeignKey("bank.id", ondelete="CASCADE"), init=False
    )
    bank: Mapped["Bank | None"] = relationship(back_populates="offices", default=None)
    atms: Mapped[list["BankAtm"]] = relationship(
        back_populates="office", default_factory=list
    )

    status: Mapped[BankOfficeStatus | None] = mapped_column(
        Enum(BankOfficeStatus), default=None
    )
