from sqlalchemy.ext.asyncio import AsyncSession
from bot.database.models import UserModel
from bot.database.services import City, Ethnicity
from bot.loader import bot
from bot.app.text import message_text as mt
from bot.app.keyboards.default.search import search_menu_kb

async def send_filter(session: AsyncSession, chat_id: int, user: UserModel) -> None:
    """Отправляет пользователю переданный в функцию профиль"""
    profile_text = await format_filter_text(session, user)

    await bot.send_message(
        chat_id=chat_id,
        text=profile_text,
        parse_mode="HTML",
    )

    await bot.send_message(chat_id=chat_id, text=mt.SEARCH_MENU, reply_markup=search_menu_kb(user))


async def format_filter_text(session: AsyncSession, user: UserModel) -> str:
    """Форматирует фильтр для отображения"""
    goal_map = {
        "friendship": mt.KB_GOAL_FRIENDSHIP,
        "communication": mt.KB_GOAL_COMMUNICATION,
        "marriage": mt.KB_GOAL_MARRIAGE,
        "serious_relationship": mt.KB_GOAL_SERIOUS_RELATIONSHIP,
    }

    def safe(value):
        return "-" if value in (None, "", " ") else value

    f = user.filter

    # Город
    city_name = "-"
    city_obj = await City.get_by_id(session, id=f.city_id)
    if city_obj:
        match user.language:
            case "uz":
                city_name = safe(city_obj.uz)
            case "en":
                city_name = safe(city_obj.en)
            case "ru":
                city_name = safe(city_obj.ru)

    # Национальность с учетом пола
    ethnicity_name = "-"
    ethnicity_obj = await Ethnicity.get_by_id(session, id=f.ethnicity_id)
    if ethnicity_obj and user.profile:
        user_gender = user.profile.gender  # 'male' или 'female'
        opposite_gender = "female" if user_gender == "male" else "male"
        field_name = f"{user.language}_{opposite_gender}"  # ru_female, en_male и т.д.
        ethnicity_name = getattr(ethnicity_obj, field_name, "-")

    # Сборка текста фильтра
    profile_text = f"""
{mt.FILTER_HEADER}

{mt.FILTER_CITY.format(city_name)}
{mt.FILTER_AGE_FROM.format(safe(f.age_from))}
{mt.FILTER_AGE_TO.format(safe(f.age_to))}
{mt.FILTER_HEIGHT_FROM.format(safe(f.height_from))}
{mt.FILTER_HEIGHT_TO.format(safe(f.height_to))}
{mt.FILTER_WEIGHT_FROM.format(safe(f.weight_from))}
{mt.FILTER_WEIGHT_TO.format(safe(f.weight_to))}
{mt.FILTER_HAS_CHILDREN.format("-" if f.has_children is None else (mt.PROFILE_YES if f.has_children else mt.PROFILE_NO))}
{mt.FILTER_GOAL.format(goal_map.get(f.goal, safe(f.goal)))}
{mt.FILTER_ETHNICITY.format(safe(ethnicity_name))}"""

    return profile_text
