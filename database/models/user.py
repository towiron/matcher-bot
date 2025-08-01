from sqlalchemy import BigInteger, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel
from data.config import CHANCE_COST, STARTER_CHANCE_COUNT


class UserStatus:
    Banned = 0
    User = 1
    Sponsor = 2
    Moderator = 3
    Admin = 4
    Owner = 5

DEFAULT_BALANCE = CHANCE_COST * STARTER_CHANCE_COUNT

class UserModel(BaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(String(70), nullable=True)
    language: Mapped[str] = mapped_column(String(10), server_default="en")
    balance: Mapped[int] = mapped_column(Integer, server_default=str(DEFAULT_BALANCE))
    status: Mapped[int] = mapped_column(Integer, server_default="1")

    profile: Mapped["ProfileModel"] = relationship(  # type: ignore
        "ProfileModel", uselist=False, back_populates="user"
    )

    filter: Mapped["FilterModel"] = relationship(  # type: ignore
        "FilterModel", uselist=False, back_populates="user"
    )
