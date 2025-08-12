from typing import Optional
from sqlalchemy import ForeignKey, Integer, String, BigInteger, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel
from .enums import EntryKind, Source

class BalanceEntryModel(BaseModel):
    __tablename__ = "balance_entries"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"))

    # что это за запись
    kind: Mapped[EntryKind] = mapped_column(Enum(EntryKind), nullable=False)
    source: Mapped[Source] = mapped_column(Enum(Source), nullable=False)

    # на сколько изменить баланс в шансах (знак важен!)
    delta_chances: Mapped[int] = mapped_column(Integer, nullable=False)

    # информативно (для платёжных записей) — сколько реально денег пришло/вернулось, в сумах
    amount_sum: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    # полезные поля для аудита/связей
    payload: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    target_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    user: Mapped["UserModel"] = relationship("UserModel", back_populates="ledger") # noqa: F821
