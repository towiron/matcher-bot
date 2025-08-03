from sqlalchemy import ForeignKey, Integer, String, BigInteger, TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import BaseModel


class UsageReason:
    ViewProfileManual = "view_profile_manual"
    ViewProfileAI = "view_profile_ai"


class BalanceUsageModel(BaseModel):
    __tablename__ = "balance_usages"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"))
    amount: Mapped[int] = mapped_column(Integer)
    reason: Mapped[str] = mapped_column(String(50))
    target_id: Mapped[str] = mapped_column(String(100), nullable=True)

    user: Mapped["UserModel"] = relationship("UserModel", back_populates="usages")
