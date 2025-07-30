from sqlalchemy.ext.asyncio import AsyncSession

from database.models import FilterModel
from database.services import City
from loader import bot
from app.text import message_text as mt
from app.keyboards.default.search import search_menu_kb

async def send_filter(session: AsyncSession, chat_id: int, filter: FilterModel, user_language: str = "ru") -> None:
    """Отправляет пользователю переданный в функцию профиль"""
    profile_text = await format_filter_text(session, filter, user_language)

    await bot.send_message(
        chat_id=chat_id,
        text=profile_text,
        parse_mode="HTML",
    )

    await bot.send_message(chat_id=chat_id, text=mt.SEARCH_MENU, reply_markup=search_menu_kb())


async def format_filter_text(session: AsyncSession, filter: FilterModel, user_language: str) -> str:
    """Форматирует фильтр для отображения"""
    goal_map = {
        "friendship": mt.KB_GOAL_FRIENDSHIP,
        "communication": mt.KB_GOAL_COMMUNICATION,
        "marriage": mt.KB_GOAL_MARRIAGE,
        "serious_relationship": mt.KB_GOAL_SERIOUS_RELATIONSHIP,
    }

    def safe(value):
        return "-" if value in (None, "", " ") else value

    city_obj = await City.get_by_id(session, id=filter.city_id)
    city_name = safe(city_obj.name_en if city_obj else "-")
    if city_obj:
        match user_language:
            case "uz":
                city_name = safe(city_obj.name_uz)
            case "en":
                city_name = safe(city_obj.name_en)
            case "ru":
                city_name = safe(city_obj.name_ru)

    profile_text = f"""
{mt.FILTER_HEADER}

{mt.FILTER_CITY.format(city_name)}
{mt.FILTER_AGE_FROM.format(safe(filter.age_from))}
{mt.FILTER_AGE_TO.format(safe(filter.age_to))}
{mt.FILTER_HEIGHT_FROM.format(safe(filter.height_from))}
{mt.FILTER_HEIGHT_TO.format(safe(filter.height_to))}
{mt.FILTER_WEIGHT_FROM.format(safe(filter.weight_from))}
{mt.FILTER_WEIGHT_TO.format(safe(filter.weight_to))}
{mt.FILTER_HAS_CHILDREN.format("-" if filter.has_children is None else (mt.PROFILE_YES if filter.has_children else mt.PROFILE_NO))}
{mt.FILTER_GOAL.format(goal_map.get(filter.goal, safe(filter.goal)))}
{mt.FILTER_ETHNICITY.format(safe(filter.ethnicity))}"""

    return profile_text

