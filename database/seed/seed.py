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
from database.models.marital_status import MaritalStatusModel

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
        CityModel(uz="Тошкент",    ru="Ташкент",    en="Tashkent"),
        CityModel(uz="Тошкент вилояти",    ru="Ташкентская область",    en="Tashkent region"),
        CityModel(uz="Самарқанд",   ru="Самарканд",  en="Samarkand"),
        CityModel(uz="Бухоро",      ru="Бухара",     en="Bukhara"),
        CityModel(uz="Хива",        ru="Хива",       en="Khiva"),
        CityModel(uz="Шаҳрисабз",  ru="Шахрисабз",  en="Shahrisabz"),
        CityModel(uz="Мўйноқ",      ru="Муйнак",     en="Muynak"),
        CityModel(uz="Заамин",       ru="Заамин",     en="Zaamin"),
        CityModel(uz="Термиз",      ru="Термез",     en="Termez"),
        CityModel(uz="Гулистон",    ru="Гулистан",   en="Gulistan"),
        CityModel(uz="Нукус",       ru="Нукус",      en="Nukus"),
        CityModel(uz="Наманган",    ru="Наманган",   en="Namangan"),
        CityModel(uz="Қарши",      ru="Карши",      en="Karshi"),
        CityModel(uz="Навоий",      ru="Навои",      en="Navoi"),
        CityModel(uz="Қўқон",      ru="Коканд",     en="Kokand"),
        CityModel(uz="Андижон",     ru="Андижан",    en="Andijan"),
        CityModel(uz="Фарғона",    ru="Фергана",    en="Fergana"),
    ]
    await seed_table(session, CityModel, cities, "cities")


async def seed_religions(session: AsyncSession):
    religions = [
        ReligionModel(uz="Ислом", ru="Ислам", en="Islam"),
        ReligionModel(uz="Насронийлик", ru="Христианство", en="Christianity"),
        ReligionModel(uz="Яҳудийлик", ru="Иудаизм", en="Judaism"),
        ReligionModel(uz="Буддизм", ru="Буддизм", en="Buddhism"),
        ReligionModel(uz="Ҳиндуийлик", ru="Индуизм", en="Hinduism"),
        ReligionModel(uz="Агностицизм", ru="Агностицизм", en="Agnosticism"),
    ]
    await seed_table(session, ReligionModel, religions, "religions")

async def seed_ethnicities(session: AsyncSession):
    ethnicities = [
        EthnicityModel(
            uz_male="Ўзбек", uz_female="Ўзбек",
            ru_male="Узбек", ru_female="Узбечка",
            en_male="Uzbek", en_female="Uzbek"
        ),
        EthnicityModel(
            uz_male="Рус", uz_female="Рус",
            ru_male="Русский", ru_female="Русская",
            en_male="Russian", en_female="Russian"
        ),
        EthnicityModel(
            uz_male="Қозоқ", uz_female="Қозоқ",
            ru_male="Казах", ru_female="Казашка",
            en_male="Kazakh", en_female="Kazakh"
        ),
        EthnicityModel(
            uz_male="Қорақалпоқ", uz_female="Қорақалпоқ",
            ru_male="Каракалпак", ru_female="Каракалпачка",
            en_male="Karakalpak", en_female="Karakalpak"
        ),
        EthnicityModel(
            uz_male="Тожик", uz_female="Тожик",
            ru_male="Таджик", ru_female="Таджичка",
            en_male="Tajik", en_female="Tajik"
        ),
        EthnicityModel(
            uz_male="Қирғиз", uz_female="Қирғиз",
            ru_male="Киргиз", ru_female="Киргизка",
            en_male="Kyrgyz", en_female="Kyrgyz"
        ),
        EthnicityModel(
            uz_male="Туркман", uz_female="Туркман",
            ru_male="Туркмен", ru_female="Туркменка",
            en_male="Turkmen", en_female="Turkmen"
        ),
        EthnicityModel(
            uz_male="Татар", uz_female="Татар",
            ru_male="Татарин", ru_female="Татарка",
            en_male="Tatar", en_female="Tatar"
        ),
        EthnicityModel(
            uz_male="Уйғур", uz_female="Уйғур",
            ru_male="Уйгур", ru_female="Уйгурка",
            en_male="Uyghur", en_female="Uyghur"
        ),
        EthnicityModel(
            uz_male="Яҳудий", uz_female="Яҳудий",
            ru_male="Еврей", ru_female="Еврейка",
            en_male="Jewish", en_female="Jewish"
        ),
        EthnicityModel(
            uz_male="Немис", uz_female="Немис",
            ru_male="Немец", ru_female="Немка",
            en_male="German", en_female="German"
        ),
        EthnicityModel(
            uz_male="Арман", uz_female="Арман",
            ru_male="Армянин", ru_female="Армянка",
            en_male="Armenian", en_female="Armenian"
        ),
        EthnicityModel(
            uz_male="Корейс", uz_female="Корейс",
            ru_male="Кореец", ru_female="Кореянка",
            en_male="Korean", en_female="Korean"
        ),
        EthnicityModel(
            uz_male="Украин", uz_female="Украин",
            ru_male="Украинец", ru_female="Украинка",
            en_male="Ukrainian", en_female="Ukrainian"
        ),
    ]

    await seed_table(session, EthnicityModel, ethnicities, "ethnicities")



async def seed_marital_statuses(session: AsyncSession):
    statuses = [
        MaritalStatusModel(
            uz_male="Бўйдок", uz_female="Турмуш қурмаган",
            ru_male="Не женат", ru_female="Не замужем",
            en_male="Single", en_female="Single"
        ),
        MaritalStatusModel(
            uz_male="Уйланган", uz_female="Турмушга чиққан",
            ru_male="Женат", ru_female="Замужем",
            en_male="Married", en_female="Married"
        ),
        MaritalStatusModel(
            uz_male="Ажрашган", uz_female="Ажрашган",
            ru_male="В разводе", ru_female="В разводе",
            en_male="Divorced", en_female="Divorced"
        ),
        MaritalStatusModel(
            uz_male="Бева", uz_female="Бева",
            ru_male="Вдовец", ru_female="Вдова",
            en_male="Widower", en_female="Widow"
        ),
    ]

    await seed_table(session, MaritalStatusModel, statuses, "marital_statuses")



async def main():
    async with async_session() as session:
        await seed_cities(session)
        await seed_ethnicities(session)
        await seed_religions(session)
        await seed_marital_statuses(session)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
