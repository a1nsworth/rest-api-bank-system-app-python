from dishka import Provider, provide, Scope
from sqlalchemy.ext.asyncio import AsyncSession

from src.services import services


class ServiceProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def get_bank(self, session: AsyncSession) -> services.BankService:
        return services.BankService(session=session)

    @provide
    def get_bank_office(self, session: AsyncSession) -> services.BankOfficeService:
        return services.BankOfficeService(session=session)

    @provide
    def get_bank_atm(self, session: AsyncSession) -> services.BankAtmService:
        return services.BankAtmService(session=session)

    @provide
    def get_user(self, session: AsyncSession) -> services.UserService:
        return services.UserService(session=session)

    @provide
    def get_employee(self, session: AsyncSession) -> services.EmployeeService:
        return services.EmployeeService(session=session)

    @provide
    def get_credit_account(
        self, session: AsyncSession
    ) -> services.CreditAccountService:
        return services.CreditAccountService(session=session)

    @provide
    def get_payment_account(
        self, session: AsyncSession
    ) -> services.PaymentAccountService:
        return services.PaymentAccountService(session=session)
