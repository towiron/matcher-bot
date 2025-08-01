import sys
from pathlib import Path

if __name__ == "__main__":
    project_root = Path(__file__).parent.parent.parent
    sys.path.insert(0, str(project_root))

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.connect import async_session
from database.models.city import CityModel
from database.models.ethnicity import EthnicityModel
from database.models.religion import ReligionModel

async def seed_table(session: AsyncSession, model, entries: list, table_name: str):
    result = await session.execute(select(model))
    if result.scalars().first():
        print(f"Таблица {table_name} уже содержит данные.")
        return

    session.add_all(entries)
    await session.commit()
    print(f"Таблица {table_name} успешно заполнена.")

async def seed_cities(session: AsyncSession):
    cities = [
        CityModel(uz="Toshkent",    ru="Ташкент",    en="Tashkent"),
        CityModel(uz="Samarqand",   ru="Самарканд",  en="Samarkand"),
        CityModel(uz="Buxoro",      ru="Бухара",     en="Bukhara"),
        CityModel(uz="Xiva",        ru="Хива",       en="Khiva"),
        CityModel(uz="Shahrisabz",  ru="Шахрисабз",  en="Shahrisabz"),
        CityModel(uz="Moynaq",      ru="Муйнак",     en="Muynak"),
        CityModel(uz="Zomin",       ru="Заамин",     en="Zaamin"),
        CityModel(uz="Termiz",      ru="Термез",     en="Termez"),
        CityModel(uz="Guliston",    ru="Гулистан",   en="Gulistan"),
        CityModel(uz="Nukus",       ru="Нукус",      en="Nukus"),
        CityModel(uz="Namangan",    ru="Наманган",   en="Namangan"),
        CityModel(uz="Qarshi",      ru="Карши",      en="Karshi"),
        CityModel(uz="Navoiy",      ru="Навои",      en="Navoi"),
        CityModel(uz="Qoʻqon",      ru="Коканд",     en="Kokand"),
        CityModel(uz="Andijon",     ru="Андижан",    en="Andijan"),
        CityModel(uz="Fargʻona",    ru="Фергана",    en="Fergana"),
    ]
    await seed_table(session, CityModel, cities, "cities")

async def seed_religions(session: AsyncSession):
    religions = [
        ReligionModel(uz="Islom", ru="Ислам", en="Islam"),
        ReligionModel(uz="Nasroniylik", ru="Христианство", en="Christianity"),
        ReligionModel(uz="Yahudiylik", ru="Иудаизм", en="Judaism"),
        ReligionModel(uz="Buddizm", ru="Буддизм", en="Buddhism"),
        ReligionModel(uz="Hinduiylik", ru="Индуизм", en="Hinduism"),
        ReligionModel(uz="Agnostitsizm", ru="Агностицизм", en="Agnosticism"),
    ]
    await seed_table(session, ReligionModel, religions, "religions")

async def seed_ethnicities(session: AsyncSession):
    ethnicities = [
        EthnicityModel(uz="O'zbek", ru="Узбек/Узбечка", en="Uzbek"),
        EthnicityModel(uz="Rus", ru="Русский/Русская", en="Russian"),
        EthnicityModel(uz="Qozoq", ru="Казах/Казашка", en="Kazakh"),
        EthnicityModel(uz="Qoraqalpoq", ru="Каракалпак/Каракалпачка", en="Karakalpak"),
        EthnicityModel(uz="Tojik", ru="Таджик/Таджичка", en="Tajik"),
        EthnicityModel(uz="Qirgʻiz", ru="Киргиз/Киргизка", en="Kyrgyz"),
        EthnicityModel(uz="Turkman", ru="Туркмен/Туркменка", en="Turkmen"),
        EthnicityModel(uz="Tatar", ru="Татарин/Татарка", en="Tatar"),
        EthnicityModel(uz="Uygʻur", ru="Уйгур/Уйгурка", en="Uyghur"),
        EthnicityModel(uz="Yahudiy", ru="Еврей/Еврейка", en="Jewish"),
        EthnicityModel(uz="Nemis", ru="Немец/Немка", en="German"),
        EthnicityModel(uz="Arman", ru="Армянин/Армянка", en="Armenian"),
        EthnicityModel(uz="Koreys", ru="Кореец/Кореянка", en="Korean"),
        EthnicityModel(uz="Ukrain", ru="Украинец/Украинка", en="Ukrainian"),
    ]
    await seed_table(session, EthnicityModel, ethnicities, "ethnicities")

async def main():
    async with async_session() as session:
        await seed_cities(session)
        await seed_ethnicities(session)
        await seed_religions(session)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
