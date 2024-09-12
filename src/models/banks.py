import random
from enum import Flag, auto

from sqlalchemy import String, ForeignKey, Enum, Date, create_engine, select
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
    Session,
)

from src.models.models import WithPK, PersonModel, Base


class BankUser(WithPK):
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    bank_id: Mapped[int] = mapped_column(ForeignKey("bank.id"))


class Bank(WithPK):
    name: Mapped[str] = mapped_column(String(100), unique=True)
    rating: Mapped[int] = mapped_column(
        default_factory=lambda: random.randint(0, 100), init=False
    )
    total_sum: Mapped[int] = mapped_column(
        default_factory=lambda: random.randint(0, int(1e6)), init=False
    )

    atms: Mapped[list["BankAtm"]] = relationship(
        back_populates="bank", default_factory=list, lazy="selectin"
    )
    offices: Mapped[list["BankOffice"]] = relationship(
        back_populates="bank", default_factory=list, lazy="selectin"
    )
    employees: Mapped[list["Employee"]] = relationship(
        back_populates="bank", default_factory=list, lazy="selectin"
    )
    users: Mapped[list["User"]] = relationship(
        back_populates="banks",
        default_factory=list,
        secondary="bank_user",
        lazy="selectin",
    )

    def count_atms(self) -> int:
        return len(self.atms)

    def count_offices(self) -> int:
        return len(self.offices)

    def count_clients(self) -> int:
        return len(self.offices)


class User(WithPK, PersonModel):
    work_place: Mapped[str | None] = mapped_column(String(100))
    bank_credit_score: Mapped[int]
    monthly_income: Mapped[float] = mapped_column(
        default_factory=lambda: round(random.uniform(0.0, 10000), 2), init=False
    )

    banks: Mapped[list["Bank"]] = relationship(
        back_populates="users",
        secondary="bank_user",
        default_factory=list,
        lazy="selectin",
    )
    credit_accounts: Mapped[list["CreditAccount"]] = relationship(
        back_populates="user", default_factory=list, lazy="selectin"
    )
    payment_accounts: Mapped[list["PaymentAccount"]] = relationship(
        back_populates="user", default_factory=list, lazy="selectin"
    )


class EmployeeStatus(Flag):
    IsRemote = auto()
    CanGiveLoans = auto()


class Employee(WithPK, PersonModel):
    position: Mapped[str] = mapped_column(String(30))
    salary: Mapped[int]

    bank_id: Mapped[int] = mapped_column(ForeignKey("bank.id"), init=False)
    office_id: Mapped[int] = mapped_column(ForeignKey("bank_office.id"), init=False)
    bank: Mapped["Bank | None"] = relationship(
        back_populates="employees", default=None, lazy="selectin"
    )
    office: Mapped["BankOffice | None"] = relationship(default=None, lazy="selectin")
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

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), init=False)
    bank_id: Mapped[int] = mapped_column(ForeignKey("bank.id"), init=False)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employee.id"), init=False)
    payment_account_id: Mapped[int] = mapped_column(
        ForeignKey("payment_account.id"), init=False
    )
    user: Mapped["User | None"] = relationship(
        back_populates="credit_accounts", default=None, lazy="selectin"
    )
    bank: Mapped["Bank | None"] = relationship(default=None, lazy="selectin")
    employee: Mapped["Employee | None"] = relationship(default=None, lazy="selectin")
    payment_account: Mapped["PaymentAccount | None"] = relationship(
        default=None, lazy="selectin"
    )


class PaymentAccount(WithPK):
    balance: Mapped[int]

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    bank_id: Mapped[int] = mapped_column(ForeignKey("bank.id"))
    user: Mapped["User | None"] = relationship(
        back_populates="payment_accounts", default=None, lazy="selectin"
    )
    bank: Mapped["Bank | None"] = relationship(default=None, lazy="selectin")


class BankAtmStatus(Flag):
    Active = auto()
    HaveMoney = auto()
    WorkToDespenseMoney = auto()
    AbleWithdraw = auto()


class BankAtm(WithPK):
    name: Mapped[str] = mapped_column(String(50))
    amortization: Mapped[int]

    bank_id: Mapped[int] = mapped_column(ForeignKey("bank.id"), init=False)
    office_id: Mapped[int] = mapped_column(ForeignKey("bank_office.id"), init=False)
    office: Mapped["BankOffice | None"] = relationship(
        back_populates="atms", default=None, lazy="selectin"
    )
    bank: Mapped["Bank | None"] = relationship(
        back_populates="atms", default=None, lazy="selectin"
    )

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

    bank_id: Mapped[int] = mapped_column(ForeignKey("bank.id"), init=False)
    bank: Mapped["Bank | None"] = relationship(
        back_populates="offices", default=None, lazy="selectin"
    )
    atms: Mapped[list["BankAtm"]] = relationship(
        back_populates="office", default_factory=list, lazy="selectin"
    )

    status: Mapped[BankOfficeStatus | None] = mapped_column(
        Enum(BankOfficeStatus), default=None
    )


def main():
    engine = create_engine("sqlite:///:memory:", echo=True)
    Base.metadata.create_all(engine)

    session = Session(engine)
    user = User(
        first_name="asd",
        second_name="123",
        patronymic_name="123",
        work_place="Moscow",
        bank_credit_score=123,
    )
    bank = Bank(name="VTB")

    bank.users.append(user)
    session.add(bank)
    session.commit()

    stmt = select(Bank)
    res = session.scalars(stmt).one_or_none()
    print(type(res))


if __name__ == "__main__":
    main()
