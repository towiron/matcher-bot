from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel

class ReligionModel(BaseModel):
    __tablename__ = "religions"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    uz: Mapped[str] = mapped_column(String(100), nullable=False)
    ru: Mapped[str] = mapped_column(String(100), nullable=False)
    en: Mapped[str] = mapped_column(String(100), nullable=False)
