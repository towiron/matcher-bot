import sys
from pathlib import Path

if __name__ == "__main__":
    project_root = Path(__file__).parent.parent.parent
    sys.path.insert(0, str(project_root))

import random
import argparse
from faker import Faker
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import ReligionModel
from database.models.user import UserModel
from database.models.profile import ProfileModel
from database.models.filter import FilterModel
from database.models.city import CityModel
from database.models.ethnicity import EthnicityModel
from database.models.marital_status import MaritalStatusModel
from database.connect import async_session

fake = Faker("ru_RU")

GENDERS = ["male", "female"]
EDUCATIONS = ["secondary", "higher"]
GOALS = ["friendship", "communication", "marriage"]
RELIGIOUS_LEVELS = ["low", "medium", "high"]
LANGUAGES = ["ru"]


async def create_fake_user(session: AsyncSession):
    cities = (await session.scalars(select(CityModel))).all()
    ethnicities = (await session.scalars(select(EthnicityModel))).all()
    religions = (await session.scalars(select(ReligionModel))).all()
    marital_statuses = (await session.scalars(select(MaritalStatusModel))).all()

    if not all([cities, ethnicities, religions, marital_statuses]):
        print("❌ Убедитесь, что все справочники (города, национальности, религии, семейные статусы) заполнены.")
        return

    city = random.choice(cities)
    ethnicity = random.choice(ethnicities)
    religion = random.choice(religions)
    marital_status = random.choice(marital_statuses)

    gender = random.choice(GENDERS)

    religious_level = random.choice(RELIGIOUS_LEVELS)
    if religion.en.lower() in ["other", "atheism", "prefer not to say"]:
        religious_level = None

    user = UserModel(
        id=fake.unique.random_int(min=10000000, max=99999999999),
        username=fake.user_name(),
        language=random.choice(LANGUAGES),
    )
    session.add(user)
    await session.flush()

    profile = ProfileModel(
        id=user.id,
        name=fake.first_name_male() if gender == "male" else fake.first_name_female(),
        age=random.randint(20, 40),
        gender=gender,
        city_id=city.id,
        height=random.randint(160, 190),
        weight=random.randint(50, 90),
        marital_status_id=marital_status.id,  # ✅ now correct
        has_children=random.choice([True, False]),
        education=random.choice(EDUCATIONS),
        goal=random.choice(GOALS),
        polygamy=random.choice([True, False, None]),
        religion_id=religion.id,
        religious_level=religious_level,
        ethnicity_id=ethnicity.id,
        job=fake.job(),
        about=fake.sentence(nb_words=12),
        looking_for="Хочу найти человека для общения",
        is_active=True
    )
    session.add(profile)

    filter_model = FilterModel(
        id=user.id,
        city_id=city.id,
        age_from=20,
        age_to=35,
        height_from=160,
        height_to=190,
        weight_from=50,
        weight_to=70,
        goal=random.choice(GOALS),
        ethnicity_id=ethnicity.id,
        has_children=random.choice([True, False, None]),
    )
    session.add(filter_model)

    await session.commit()
    print(f"✅ Пользователь {user.username} создан.")


async def main(count: int):
    async with async_session() as session:
        for _ in range(count):
            await create_fake_user(session)


if __name__ == "__main__":
    import asyncio

    parser = argparse.ArgumentParser(description="Создание фейковых пользователей")
    parser.add_argument("--count", type=int, default=1, help="Количество пользователей для создания")
    args = parser.parse_args()

    asyncio.run(main(args.count))
