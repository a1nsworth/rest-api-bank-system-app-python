from typing import Annotated

from inflection import underscore
from sqlalchemy import String, Date
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import (
    DeclarativeBase,
    declared_attr,
    Mapped,
    mapped_column,
    MappedAsDataclass,
)

type PrimaryKey = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]


class Base(DeclarativeBase, AsyncAttrs):
    __abstract__ = True

    @declared_attr
    def __tablename__(cls) -> str:
        return underscore(cls.__name__)


class WithPK(MappedAsDataclass, Base):
    __abstract__ = True
    id: Mapped[int] = mapped_column(
        primary_key=True, unique=True, autoincrement=True, init=False
    )


class PersonModel(MappedAsDataclass, Base):
    __abstract__ = True
    first_name: Mapped[str] = mapped_column(String(30))
    second_name: Mapped[str] = mapped_column(String(30))
    patronymic_name: Mapped[str | None] = mapped_column(String(30))
    date_of_birth = mapped_column(Date)
