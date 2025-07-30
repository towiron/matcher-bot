from database.models import FilterModel
from loader import bot
from app.text import message_text as mt


async def send_filter(chat_id: int, filter: FilterModel) -> None:
    """Отправляет пользователю переданный в функцию профиль"""
    profile_text = format_filter_text(filter)

    await bot.send_message(
        chat_id=chat_id,
        text=profile_text,
        parse_mode="HTML",
    )


def format_filter_text(filter: FilterModel) -> str:
    """Форматирует профиль для отображения"""
    goal_map = {
        "friendship": mt.KB_GOAL_FRIENDSHIP,
        "communication": mt.KB_GOAL_COMMUNICATION,
        "marriage": mt.KB_GOAL_MARRIAGE,
        "serious_relationship": mt.KB_GOAL_SERIOUS_RELATIONSHIP,
    }

    # Сборка текста
    profile_text = f"""
{mt.FILTER_HEADER}

{mt.FILTER_CITY.format(filter.city)}
{mt.FILTER_AGE_FROM.format(filter.age_from)}
{mt.FILTER_AGE_TO.format(filter.age_to)}
{mt.FILTER_HEIGHT_FROM.format(filter.height_from)}
{mt.FILTER_HEIGHT_TO.format(filter.height_to)}
{mt.FILTER_WEIGHT_FROM.format(filter.weight_from)}
{mt.FILTER_WEIGHT_TO.format(filter.weight_from)}
{mt.FILTER_HAS_CHILDREN.format(mt.PROFILE_YES if filter.has_children else mt.PROFILE_NO)}
{mt.FILTER_GOAL.format(goal_map.get(filter.goal, filter.goal))}
{mt.FILTER_ETHNICITY.format(filter.ethnicity)}"""

    return profile_text
