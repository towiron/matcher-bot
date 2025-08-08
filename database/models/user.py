from datetime import date
from typing import Optional
from sqlalchemy import BigInteger, Integer, String, Boolean, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import BaseModel
from .enums import UserStatus

class UserModel(BaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[Optional[str]] = mapped_column(String(70), nullable=True)
    language: Mapped[str] = mapped_column(String(10), server_default="en")
    status: Mapped[int] = mapped_column(Integer, server_default=str(int(UserStatus.User)))
    accepted_offer: Mapped[bool] = mapped_column(Boolean, server_default="false", nullable=False)

    # Баланс в шансах (кеш)
    balance_chances: Mapped[int] = mapped_column(Integer, server_default="0", nullable=False)

    # Ежедневка/стрик
    last_active_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    daily_streak: Mapped[int] = mapped_column(Integer, server_default="0", nullable=False)

    # Леджер движений
    ledger: Mapped[list["BalanceEntryModel"]] = relationship(
        "BalanceEntryModel", back_populates="user", cascade="all, delete-orphan"
    )

    # 1:1 связи
    profile: Mapped["ProfileModel"] = relationship("ProfileModel", uselist=False, back_populates="user")
    filter:  Mapped["FilterModel"]  = relationship("FilterModel",  uselist=False, back_populates="user")
