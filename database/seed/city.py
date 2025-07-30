import sys
from pathlib import Path

if __name__ == "__main__":
    project_root = Path(__file__).parent.parent.parent
    sys.path.insert(0, str(project_root))

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.connect import async_session
from database.models.city import CityModel

async def seed_cities():
    async with async_session() as session:  # type: AsyncSession
        result = await session.execute(select(CityModel))
        if result.scalars().first():
            print("Таблица cities уже содержит данные.")
            return

        cities = [
            CityModel(name_uz="Toshkent",    name_ru="Ташкент",    name_en="Tashkent"),
            CityModel(name_uz="Samarqand",   name_ru="Самарканд",  name_en="Samarkand"),
            CityModel(name_uz="Buxoro",      name_ru="Бухара",     name_en="Bukhara"),
            CityModel(name_uz="Xiva",        name_ru="Хива",       name_en="Khiva"),
            CityModel(name_uz="Shahrisabz",  name_ru="Шахрисабз",  name_en="Shahrisabz"),
            CityModel(name_uz="Moynaq",      name_ru="Муйнак",     name_en="Muynak"),
            CityModel(name_uz="Zomin",       name_ru="Заамин",     name_en="Zaamin"),
            CityModel(name_uz="Termiz",      name_ru="Термез",     name_en="Termez"),
            CityModel(name_uz="Guliston",    name_ru="Гулистан",   name_en="Gulistan"),
            CityModel(name_uz="Nukus",       name_ru="Нукус",      name_en="Nukus"),
            CityModel(name_uz="Namangan",    name_ru="Наманган",   name_en="Namangan"),
            CityModel(name_uz="Qarshi",      name_ru="Карши",      name_en="Karshi"),
            CityModel(name_uz="Navoiy",      name_ru="Навои",      name_en="Navoi"),
            CityModel(name_uz="Qoʻqon",      name_ru="Коканд",     name_en="Kokand"),
            CityModel(name_uz="Andijon",     name_ru="Андижан",    name_en="Andijan"),
            CityModel(name_uz="Fargʻona",    name_ru="Фергана",    name_en="Fergana"),
        ]

        session.add_all(cities)
        await session.commit()
        print("Таблица cities успешно заполнена.")

if __name__ == "__main__":
    import asyncio
    asyncio.run(seed_cities())