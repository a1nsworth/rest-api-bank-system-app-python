from fastapi import Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import sqlite_db_helper
from src.repositories.repositories import BankAsyncRepository, BankOfficeAsyncRepository

from src.services.bank import BankService, BankOfficeService


async def get_bank_service(
    session: Annotated[AsyncSession, Depends(sqlite_db_helper.get_session)]
) -> BankService:
    return BankService(session, BankAsyncRepository(session))


async def get_office_service(
    session: Annotated[AsyncSession, Depends(sqlite_db_helper.get_session)]
) -> BankOfficeService:
    return BankOfficeService(session, BankOfficeAsyncRepository(session))
