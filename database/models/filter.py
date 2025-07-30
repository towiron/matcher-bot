from sqlalchemy import BigInteger, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel


class FilterModel(BaseModel):
    __tablename__ = "filters"

    # ID пользователя (одновременно первичный ключ и внешний ключ к users.id)
    id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )

    # Город для поиска (опционально)
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"), nullable=True)

    # Минимальный возраст для поиска
    age_from: Mapped[int] = mapped_column(Integer, nullable=True)

    # Максимальный возраст для поиска
    age_to: Mapped[int] = mapped_column(Integer, nullable=True)

    # Минимальный рост
    height_from: Mapped[int] = mapped_column(Integer, nullable=True)

    # Максимальный рост
    height_to: Mapped[int] = mapped_column(Integer, nullable=True)

    # Минимальный вес
    weight_from: Mapped[int] = mapped_column(Integer, nullable=True)

    # Максимальный вес
    weight_to: Mapped[int] = mapped_column(Integer, nullable=True)

    # Цель знакомства
    goal: Mapped[str] = mapped_column(String(50), nullable=True)

    # Национальность
    ethnicity: Mapped[str] = mapped_column(String(50), nullable=True)

    # Наличие детей
    has_children: Mapped[bool] = mapped_column(nullable=True)

    # Связь с пользователем
    user: Mapped["UserModel"] = relationship("UserModel", back_populates="filter")  # type: ignore
    city: Mapped["CityModel"] = relationship("CityModel") # type: ignore

