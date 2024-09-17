from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories import repositories


class RepositoryProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def get_bank(self, session: AsyncSession) -> repositories.BankRepository:
        return repositories.BankRepository(session=session)

    @provide
    def get_bank_office(
        self, session: AsyncSession
    ) -> repositories.BankOfficeRepository:
        return repositories.BankOfficeRepository(session=session)

    @provide
    def get_bank_atm(self, session: AsyncSession) -> repositories.BankAtmRepository:
        return repositories.BankAtmRepository(session=session)

    @provide
    def get_user(self, session: AsyncSession) -> repositories.UserRepository:
        return repositories.UserRepository(session=session)

    @provide
    def get_employee(self, session: AsyncSession) -> repositories.EmployeeRepository:
        return repositories.EmployeeRepository(session=session)

    @provide
    def get_credit_account(
        self, session: AsyncSession
    ) -> repositories.CreditAccountRepository:
        return repositories.CreditAccountRepository(session=session)

    @provide
    def get_payment_account(
        self, session: AsyncSession
    ) -> repositories.PaymentAccountRepository:
        return repositories.PaymentAccountRepository(session=session)
