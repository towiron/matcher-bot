from app.keyboards.inline.admin import block_user_ikb
from app.text import message_text as mt
from data.config import MODERATOR_GROUP
from database.models.profile import ProfileModel
from database.models.user import UserModel
from loader import bot
from utils.logging import logger

async def send_profile(chat_id: int, profile: ProfileModel) -> None:
    """Отправляет пользователю переданный в функцию профиль"""
    profile_text = format_profile_text(profile)

    await bot.send_message(
        chat_id=chat_id,
        text=profile_text,
        parse_mode="HTML",
    )


async def complaint_to_profile(
    complainant: UserModel, reason: str, complaint_user: UserModel
) -> None:
    """Отправляет в группу модераторов анкету пользователя
    на которого пришла жалоба"""
    if MODERATOR_GROUP:
        try:
            await send_profile(MODERATOR_GROUP, complaint_user.profile)

            text = mt.REPORT_TO_USER.format(
                complainant.id,
                complainant.username,
                complaint_user.id,
                complaint_user.username,
                reason,
            )

            await bot.send_message(
                chat_id=MODERATOR_GROUP,
                text=text,
                reply_markup=block_user_ikb(
                    id=complaint_user.id,
                    username=complaint_user.username,
                ),
            )
        except:
            logger.error("Сообщение в модераторскую группу не отправленно")


def format_profile_text(profile: ProfileModel) -> str:
    """Форматирует профиль для отображения"""

    # Используем значения напрямую из message_text
    gender_map = {
        "male": mt.KB_GENDER_MALE,
        "female": mt.KB_GENDER_FEMALE,
    }

    marital_status_map = {
        "single": mt.KB_MARITAL_STATUS_SINGLE,
        "divorced": mt.KB_MARITAL_STATUS_DIVORCED,
        "widowed": mt.KB_MARITAL_STATUS_WIDOWED,
    }

    education_map = {
        "primary": mt.KB_EDUCATION_SECONDARY,  # или добавь KB_EDUCATION_PRIMARY
        "secondary": mt.KB_EDUCATION_SECONDARY,
        "incomplete_higher": mt.KB_EDUCATION_INCOMPLETE_HIGHER,
        "higher": mt.KB_EDUCATION_HIGHER,
    }

    goal_map = {
        "friendship": mt.KB_GOAL_FRIENDSHIP,
        "communication": mt.KB_GOAL_COMMUNICATION,
        "marriage": mt.KB_GOAL_MARRIAGE,
        "serious_relationship": mt.KB_GOAL_SERIOUS_RELATIONSHIP,
    }

    religion_map = {
        "islam": mt.KB_RELIGION_ISLAM,
        "christianity": mt.KB_RELIGION_CHRISTIANITY,
        "judaism": mt.KB_RELIGION_JUDAISM,
        "buddhism": mt.KB_RELIGION_BUDDHISM,
        "other": mt.KB_RELIGION_OTHER,
    }

    religious_level_map = {
        "low": mt.KB_RELIGIOSITY_LOW,
        "medium": mt.KB_RELIGIOSITY_MEDIUM,
        "high": mt.KB_RELIGIOSITY_HIGH,
        "strict": mt.KB_RELIGIOSITY_STRICT,
        "none": mt.KB_RELIGIOSITY_NONE,
    }

    # Сборка текста
    profile_text = f"""
{mt.PROFILE_HEADER}

{mt.PROFILE_NAME.format(profile.name)}
{mt.PROFILE_SURNAME.format(profile.surname)}
{mt.PROFILE_AGE.format(profile.age)}
{mt.PROFILE_GENDER.format(gender_map.get(profile.gender, profile.gender))}
{mt.PROFILE_CITY.format(profile.city)}
{mt.PROFILE_HEIGHT.format(profile.height)}
{mt.PROFILE_WEIGHT.format(profile.weight)}

{mt.PROFILE_MARITAL_STATUS.format(marital_status_map.get(profile.marital_status, profile.marital_status))}
{mt.PROFILE_HAS_CHILDREN.format(mt.PROFILE_YES if profile.has_children else mt.PROFILE_NO)}"""

    if profile.has_children and profile.children_lives_with_me is not None:
        profile_text += f"\n{mt.PROFILE_CHILDREN_LIVE_WITH_ME.format(mt.PROFILE_YES if profile.children_lives_with_me else mt.PROFILE_NO)}"

    profile_text += f"""
{mt.PROFILE_EDUCATION.format(education_map.get(profile.education, profile.education))}
{mt.PROFILE_JOB.format(profile.job or mt.PROFILE_NOT_SPECIFIED)}
{mt.PROFILE_GOAL.format(goal_map.get(profile.goal, profile.goal))}
{mt.PROFILE_POLYGAMY.format(mt.PROFILE_YES if profile.polygamy else mt.PROFILE_NO)}
{mt.PROFILE_RELIGION.format(religion_map.get((profile.religion or "").lower(), profile.religion))}"""

    if profile.religious_level:
        profile_text += f"\n{mt.PROFILE_RELIGIOUS_LEVEL.format(religious_level_map.get(profile.religious_level))}"

    profile_text += f"""
{mt.PROFILE_ETHNICITY.format(profile.ethnicity)}"""
    profile_text += f"""
{mt.PROFILE_ABOUT.format(profile.about)}"""
    profile_text += f"""
{mt.PROFILE_LOOKING_FOR.format(profile.looking_for)}"""

    return profile_text