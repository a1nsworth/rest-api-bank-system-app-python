from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import db_helper

from src.services.services import UserService, BankService, BankOfficeService


async def get_bank_service(
    session: Annotated[AsyncSession, Depends(db_helper.get_async_session)]
) -> BankService:
    return BankService(session)


async def get_user_service(
    session: Annotated[AsyncSession, Depends(db_helper.get_async_session)]
) -> UserService:
    return UserService(session)


async def get_office_service(
    session: Annotated[AsyncSession, Depends(db_helper.get_async_session)]
) -> BankOfficeService:
    return BankOfficeService(session)
