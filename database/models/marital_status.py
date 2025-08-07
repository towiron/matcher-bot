from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel

class MaritalStatusModel(BaseModel):
    __tablename__ = "marital_statuses"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    uz_male: Mapped[str] = mapped_column(String(100), nullable=False)
    uz_female: Mapped[str] = mapped_column(String(100), nullable=False)

    ru_male: Mapped[str] = mapped_column(String(100), nullable=False)
    ru_female: Mapped[str] = mapped_column(String(100), nullable=False)

    en_male: Mapped[str] = mapped_column(String(100), nullable=False)
    en_female: Mapped[str] = mapped_column(String(100), nullable=False)
