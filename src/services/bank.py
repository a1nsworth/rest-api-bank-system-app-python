from src.models.banks import Bank, BankOffice
from src.repositories.repositories import BankAsyncRepository, BankOfficeAsyncRepository
from src.services.services import BaseAsyncCRUDService


class BankService(BaseAsyncCRUDService[Bank, BankAsyncRepository]):
    async def get_by_name(self, name: str) -> Bank | None:
        return await self._repository.get_by_name(name)


class BankOfficeService(BaseAsyncCRUDService[BankOffice, BankOfficeAsyncRepository]):
    pass
