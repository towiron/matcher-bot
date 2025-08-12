from sqlalchemy import BigInteger, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel


class ProfileModel(BaseModel):
    __tablename__ = "profiles"

    # ID пользователя (одновременно первичный ключ и внешний ключ к users.id)
    id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )

    # Имя (отображается другим пользователям)
    name: Mapped[str] = mapped_column(String(200), nullable=False)

    # Возраст (может храниться отдельно для оптимизации фильтрации)
    age: Mapped[int] = mapped_column(Integer, nullable=False)

    # Пол пользователя: 'male' или 'female'
    gender: Mapped[str] = mapped_column(String(20), nullable=False)

    # Город проживания
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"), nullable=False)

    # Рост пользователя в сантиметрах
    height: Mapped[int] = mapped_column(Integer, nullable=False)

    # Вес пользователя в килограммах
    weight: Mapped[int] = mapped_column(Integer, nullable=False)

    # Семейное положение: 'single', 'divorced', 'widowed'
    marital_status_id: Mapped[int] = mapped_column(ForeignKey("marital_statuses.id"), nullable=False)

    # Есть ли дети
    has_children: Mapped[bool] = mapped_column(nullable=False)

    # Образование: 'none', 'secondary', 'higher'
    education: Mapped[str] = mapped_column(String(50), nullable=False)

    # Цель знакомства: 'friendship', 'communication', 'marriage'
    goal: Mapped[str] = mapped_column(String(50), nullable=False)

    # Приемлет ли пользователь многожёнство или NULL (если полигамность = "Not Sure")
    polygamy: Mapped[bool] = mapped_column(nullable=True)

    # Религия: например, 'Islam', 'Christianity', 'Other' и т.д.
    religion_id: Mapped[int] = mapped_column(ForeignKey("religions.id"), nullable=False)

    # Уровень религиозности: 'low', 'medium', 'high' или NULL (если религия = 'Other')
    religious_level: Mapped[str] = mapped_column(String(20), nullable=True)

    # Национальность (основное значение, например, 'Uzbek')
    ethnicity_id: Mapped[int] = mapped_column(ForeignKey("ethnicities.id"), nullable=False)

    # Профессия или вид деятельности (опционально)
    job: Mapped[str] = mapped_column(String(100), nullable=True)

    # О себе
    about: Mapped[str] = mapped_column(String(300), nullable=True)

    # Кого пользователь ищет
    looking_for: Mapped[str] = mapped_column(String(300), nullable=True)

    # Активен ли профиль (может использоваться для временного скрытия)
    is_active: Mapped[bool] = mapped_column(default=True)

    # Связь с пользователем
    user: Mapped["UserModel"] = relationship("UserModel", back_populates="profile")  # type: ignore # noqa: F821
    city: Mapped["CityModel"] = relationship("CityModel") # type: ignore # noqa: F821
    ethnicity: Mapped["EthnicityModel"] = relationship("EthnicityModel") # type: ignore # noqa: F821
    marital_status: Mapped["MaritalStatusModel"] = relationship("MaritalStatusModel")  # type: ignore # noqa: F821
    religion: Mapped["ReligionModel"] = relationship("ReligionModel") # type: ignore # noqa: F821