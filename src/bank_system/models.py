import random
from datetime import date

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.models import WithPK, Base


class Bank(WithPK):
    name: Mapped[str] = mapped_column(String(100), unique=True)
    rating: Mapped[int] = mapped_column(default_factory=lambda: random.randint(0, 100))
    total_sum: Mapped[int] = mapped_column(default_factory=lambda: random.randint(0, int(1e6)))

    atms: Mapped[list['BankAtm']] = relationship(back_populates='bank', uselist=True)
    offices: Mapped[list['Office']] = relationship(back_populates='address', uselist=True)
    clients: Mapped[list['Client']] = relationship(back_populates='bank', uselist=True)

    def count_atms(self) -> int:
        return len(self.atms)

    def count_offices(self) -> int:
        return len(self.offices)

    def count_clients(self) -> int:
        return len(self.offices)


class BankClient(Base):
    client_id = mapped_column(ForeignKey('client.id'), primary_key=True)
    bank_id = mapped_column(ForeignKey('bank.id'), primary_key=True)


class Client(WithPK):
    first_name: Mapped[str] = mapped_column(String(200))
    second_name: Mapped[str] = mapped_column(String(200))
    patronymic_name: Mapped[str] = mapped_column(String(200), nullable=True)
    birthdate: Mapped[date]

    work_place: Mapped[str] = mapped_column(String(100), nullable=True)
    monthly_income: Mapped[float] = mapped_column(
        default_factory=lambda: round(random.uniform(0.0, 10000), 2)
    )

    rating: Mapped[int] = ...


class BankAtm(WithPK):
    name: Mapped[str] = mapped_column(String(50))

    bank: Mapped['bank'] = relationship(back_populates='atms', uselist=False)
    bank_id: Mapped[int] = mapped_column(ForeignKey('bank.id'))

    total_sum: Mapped[int] = mapped_column(ForeignKey('bank.total_sum'))


class Office(WithPK):
    name: Mapped[str] = mapped_column(String(100))
    address: Mapped[str] = mapped_column(ForeignKey('bank.name'))


def eval_rating(context):
    return context.get_current_parameters()['']
