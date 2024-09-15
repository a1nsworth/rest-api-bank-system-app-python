from pydantic import BaseModel

from src.models.models import BankOfficeStatus


class PersonModel(BaseModel):
    first_name: str
    second_name: str
    patronymic_name: str | None


class BankCreate(BaseModel):
    name: str


class BankUpdate(BaseModel):
    name: str
    new_name: str


class UserCreate(PersonModel):
    work_place: str | None


class ConnectUserToBanks(BaseModel):
    id: int
    names: list[str]


class BankOfficeCreate(BaseModel):
    name: str
    rental: int
    owner: str
    status: BankOfficeStatus | None = None
