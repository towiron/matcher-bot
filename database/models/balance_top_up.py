from sqlalchemy import ForeignKey, Integer, String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import BaseModel


class TopUpSource:
    Click = "click"
    Payme = "payme"
    Uzum = "uzum"
    Initial = "initial"
    Internal = "internal"


class BalanceTopUpModel(BaseModel):
    __tablename__ = "balance_top_ups"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"))

    amount: Mapped[int] = mapped_column(Integer)  # в шансах
    paid_sum: Mapped[int] = mapped_column(Integer)  # в сумах
    source: Mapped[str] = mapped_column(String(20))  # click, payme
    payload: Mapped[str] = mapped_column(String(100), nullable=True)

    user: Mapped["UserModel"] = relationship("UserModel", back_populates="top_ups")
