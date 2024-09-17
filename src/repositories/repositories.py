from advanced_alchemy.repository import SQLAlchemyAsyncRepository

from src.models.models import (
    Bank,
    BankOffice,
    User,
    Employee,
    CreditAccount,
    PaymentAccount,
    BankAtm,
)


class BankRepository(SQLAlchemyAsyncRepository[Bank]):
    model_type = Bank


class BankOfficeRepository(SQLAlchemyAsyncRepository[BankOffice]):
    model_type = BankOffice


class BankAtmRepository(SQLAlchemyAsyncRepository[BankAtm]):
    model_type = BankAtm


class UserRepository(SQLAlchemyAsyncRepository[User]):
    model_type = User


class EmployeeRepository(SQLAlchemyAsyncRepository[Employee]):
    model_type = Employee


class CreditAccountRepository(SQLAlchemyAsyncRepository[CreditAccount]):
    model_type = CreditAccount


class PaymentAccountRepository(SQLAlchemyAsyncRepository[PaymentAccount]):
    model_type = PaymentAccount
