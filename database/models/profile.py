from sqlalchemy import BigInteger, CheckConstraint, ForeignKey, Integer, String
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

    # Фамилия (не отображается другим пользователям)
    surname: Mapped[str] = mapped_column(String(200), nullable=False)

    # Возраст (может храниться отдельно для оптимизации фильтрации)
    age: Mapped[int] = mapped_column(Integer, nullable=False)

    # Пол пользователя: 'male' или 'female'
    gender: Mapped[str] = mapped_column(String(20), nullable=False)

    # Город проживания
    city: Mapped[str] = mapped_column(String(200), nullable=False)

    # Географическая широта города (для геопоиска)
    latitude: Mapped[float] = mapped_column(nullable=False)

    # Географическая долгота города
    longitude: Mapped[float] = mapped_column(nullable=False)

    # Рост пользователя в сантиметрах
    height: Mapped[int] = mapped_column(Integer, nullable=False)

    # Вес пользователя в килограммах
    weight: Mapped[int] = mapped_column(Integer, nullable=False)

    # Семейное положение: 'single', 'divorced', 'widowed'
    marital_status: Mapped[str] = mapped_column(String(50), nullable=False)

    # Есть ли дети
    has_children: Mapped[bool] = mapped_column(nullable=False)

    # Живут ли дети с пользователем (может быть null, если has_children = False)
    children_lives_with_me: Mapped[bool] = mapped_column(nullable=True)

    # Образование: 'none', 'secondary', 'higher'
    education: Mapped[str] = mapped_column(String(50), nullable=False)

    # Цель знакомства: 'friendship', 'communication', 'marriage'
    goal: Mapped[str] = mapped_column(String(50), nullable=False)

    # Приемлет ли пользователь многожёнство или NULL (если полигамность = "Not Sure")
    polygamy: Mapped[bool] = mapped_column(nullable=True)

    # Религия: например, 'Islam', 'Christianity', 'Other' и т.д.
    religion: Mapped[str] = mapped_column(String(50), nullable=False)

    # Уровень религиозности: 'low', 'medium', 'high' или NULL (если религия = 'Other')
    religious_level: Mapped[str] = mapped_column(String(20), nullable=True)

    # Национальность (основное значение, например, 'Uzbek')
    ethnicity: Mapped[str] = mapped_column(String(50), nullable=False)

    # Профессия или вид деятельности (опционально)
    job: Mapped[str] = mapped_column(String(100), nullable=True)

    # Активен ли профиль (может использоваться для временного скрытия)
    is_active: Mapped[bool] = mapped_column(default=True)

    # Связь с пользователем
    user: Mapped["UserModel"] = relationship("UserModel", back_populates="profile")  # type: ignore

    # Ограничения на уровне базы данных
    # __table_args__ = (
    #     # Пол может быть только 'male' или 'female'
    #     CheckConstraint("gender IN ('male', 'female')", name="gender_check"),
    #
    #     # Допустимые значения для семейного положения
    #     CheckConstraint("marital_status IN ('single', 'divorced', 'widowed')", name="marital_status_check"),
    #
    #     # Допустимые значения для образования
    #     CheckConstraint("education IN ('none', 'secondary', 'higher')", name="education_check"),
    #
    #     # Допустимые цели знакомства
    #     CheckConstraint("goal IN ('friendship', 'communication', 'marriage')", name="goal_check"),
    #
    #     # Религиозность может быть NULL или одним из допустимых уровней
    #     CheckConstraint("religious_level IS NULL OR religious_level IN ('low', 'medium', 'high')", name="religious_level_check"),
    # )
