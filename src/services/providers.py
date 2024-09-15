from dishka import Provider, provide, Scope

from src.services.services import BankService, BankOfficeService, UserService


class ServiceProvider(Provider):
    scope = Scope.REQUEST
    bank = provide(BankService)
    bank_office = provide(BankOfficeService)
    user = provide(UserService)
