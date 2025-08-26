from aiogram.exceptions import TelegramForbiddenError, TelegramBadRequest, TelegramNetworkError, TelegramAPIError

from app.keyboards.default.base import search_kb
from app.keyboards.inline.admin import block_user_ikb
from app.text import message_text as mt
from data.config import MODERATOR_GROUP
from database.models.profile import ProfileModel
from database.models.user import UserModel
from database.services import City, Ethnicity, Religion
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup
from app.keyboards.inline.contact import contact_user_ikb
from database.services import User

from database.services.marital_status import MaritalStatus
from loader import bot
from utils.logging import logger

async def update_user_username_from_telegram(session: AsyncSession, user_id: int) -> str | None:
    """
    Получает актуальный username пользователя из Telegram и обновляет его в базе данных.
    Возвращает актуальный username или None, если не удалось получить.
    """
    try:
        # Получаем информацию о пользователе из Telegram
        chat_member = await bot.get_chat_member(chat_id=user_id, user_id=user_id)
        if chat_member and chat_member.user and chat_member.user.username:
            new_username = chat_member.user.username
            
            # Получаем пользователя из базы данных
            user_obj = await User.get_by_id(session, user_id)
            if user_obj and user_obj.username != new_username:
                # Обновляем username в базе данных
                await User.update_username(session, user_id, new_username)
                logger.log("USERNAME_UPDATE", f"Обновлен username для пользователя {user_id}: {user_obj.username} -> {new_username}")
            
            return new_username
        else:
            # У пользователя нет username
            user_obj = await User.get_by_id(session, user_id)
            if user_obj and user_obj.username is not None:
                # Очищаем username в базе данных
                await User.update_username(session, user_id, None)
                logger.log("USERNAME_UPDATE", f"Очищен username для пользователя {user_id}")
            
            return None
            
    except TelegramForbiddenError:
        logger.warning(f"Не удалось получить информацию о пользователе {user_id}: бот заблокирован пользователем")
        return None
    except TelegramBadRequest as e:
        logger.warning(f"Ошибка при получении информации о пользователе {user_id}: {e}")
        return None
    except Exception as e:
        logger.error(f"Неожиданная ошибка при обновлении username для пользователя {user_id}: {e}")
        return None

async def send_profile(session: AsyncSession, chat_id: int, profile: ProfileModel, user_language: str = "ru", reply_markup: ReplyKeyboardMarkup | InlineKeyboardMarkup | None = None) -> None:
    """Отправляет пользователю переданный в функцию профиль"""
    profile_text = await format_profile_text(session, profile, user_language)

    await bot.send_message(
        chat_id=chat_id,
        text=profile_text,
        parse_mode="HTML",
        reply_markup=reply_markup,
    )


async def display_filtered_profile(session: AsyncSession, chat_id: int, profile: ProfileModel, user_language: str = "ru", current_user_id: int = None) -> None:
    """Отправляет профиль пользователя которые подошли по фильтрам (работает для обычного и умного поиска)"""
    text = await format_candidate_profile_text(session, profile, user_language)
    
    # Проверяем, давал ли текущий пользователь шанс этому профилю
    reply_markup = search_kb()
    
    if current_user_id and profile.id != current_user_id:
        from database.services import Match
        from app.keyboards.inline.contact import contact_user_ikb
        from utils.logging import logger
        
        # Проверяем, давал ли пользователь шанс этому профилю
        existing_match = await Match.get(session, receiver_id=profile.id, sender_id=current_user_id)
        
        if existing_match:
            # Если пользователь уже дал шанс, показываем клавиатуру без "дать шанс"
            from app.keyboards.default.base import search_kb_after_chance
            reply_markup = search_kb_after_chance()
            # Добавляем inline-кнопку для связи
            try:
                # Обновляем username пользователя из Telegram перед формированием кнопки
                updated_username = await update_user_username_from_telegram(session, profile.id)
                
                if updated_username:
                    profile_link = f"https://t.me/{updated_username}"
                else:
                    profile_link = f"tg://user?id={profile.id}"
                
                # Создаем inline-клавиатуру для связи
                inline_markup = contact_user_ikb(user_language, profile_link)

                # Отправляем сообщение с inline-клавиатурой
                await bot.send_message(
                    chat_id=chat_id,
                    text=text,
                    parse_mode="HTML",
                    reply_markup=reply_markup,
                    disable_web_page_preview=True,
                )
                
                # Отправляем отдельное сообщение с inline-кнопкой связи
                await bot.send_message(
                    chat_id=chat_id,
                    text="💬 Вы уже дали шанс этому пользователю. Можете связаться с ним:",
                    reply_markup=inline_markup,
                )
                return
                
            except Exception as e:
                # Если не удалось создать кнопку связи, показываем информативное сообщение
                await bot.send_message(
                    chat_id=chat_id,
                    text=text,
                    parse_mode="HTML",
                    reply_markup=reply_markup,
                    disable_web_page_preview=True,
                )
                
                # Отправляем сообщение о приватном аккаунте
                await bot.send_message(
                    chat_id=chat_id,
                    text="🔒 У этого пользователя приватный аккаунт, но он может связаться с вами сам, если захочет ответить взаимностью на ваш шанс.",
                    reply_markup=reply_markup,
                )
                return

    await bot.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode="HTML",
        reply_markup=reply_markup,
        disable_web_page_preview=True,
    )


async def complaint_to_profile(
    session: AsyncSession, complainant: UserModel, reason: str, complaint_user: UserModel
) -> None:
    """Отправляет в группу модераторов анкету пользователя, на которого пришла жалоба."""
    if not MODERATOR_GROUP:
        return

    if not complaint_user.profile:
        logger.warning(f"Жалоба на {complaint_user.id}, но профиль отсутствует.")
        return

    # 1) сначала отправляем сам профиль
    try:
        await send_profile(session, MODERATOR_GROUP, complaint_user.profile, complaint_user.language)
    except TelegramForbiddenError:
        logger.error("Нет доступа к модераторской группе (бот заблокирован/удалён).")
        return
    except TelegramBadRequest as e:
        logger.error(f"BadRequest при отправке профиля: {e!r}")
        return
    except TelegramNetworkError as e:
        logger.warning(f"Сетевая ошибка при отправке профиля: {e!r}")
        return
    except TelegramAPIError as e:
        logger.exception(f"Ошибка Telegram API при отправке профиля: {e!r}")
        return

    # 2) затем текст с кнопкой блокировки
    text = mt.REPORT_TO_USER.format(
        complainant.id,
        complainant.username,
        complaint_user.id,
        complaint_user.username,
        reason,
    )

    try:
        await bot.send_message(
            chat_id=MODERATOR_GROUP,
            text=text,
            reply_markup=block_user_ikb(
                id=complaint_user.id,
                username=complaint_user.username,
            ),
        )
    except TelegramForbiddenError:
        logger.error("Нет доступа к модераторской группе (бот заблокирован/удалён).")
    except TelegramBadRequest as e:
        logger.error(f"BadRequest при отправке в модераторскую группу: {e!r}")
    except TelegramNetworkError as e:
        logger.warning(f"Сетевая ошибка при отправке в модераторскую группу: {e!r}")
    except TelegramAPIError as e:
        logger.exception(f"Ошибка Telegram API при отправке в модераторскую группу: {e!r}")


async def format_profile_text(session: AsyncSession, profile: ProfileModel, user_language: str = "ru") -> str:
    """Форматирует профиль для отображения"""

    # Используем значения напрямую из message_text
    gender_map = {
        "male": mt.KB_GENDER_MALE,
        "female": mt.KB_GENDER_FEMALE,
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

    religious_level_map = {
        "low": mt.KB_RELIGIOSITY_LOW,
        "medium": mt.KB_RELIGIOSITY_MEDIUM,
        "high": mt.KB_RELIGIOSITY_HIGH,
        "strict": mt.KB_RELIGIOSITY_STRICT,
        "none": mt.KB_RELIGIOSITY_NONE,
    }

    marital_status_obj = await MaritalStatus.get_by_id(session, id=profile.marital_status_id)
    marital_status_name = get_gendered_field_value(marital_status_obj, user_language, profile.gender)

    city_obj = await City.get_by_id(session, id=profile.city_id)
    city_name = city_obj.en
    if city_obj:
        match user_language:
            case "uz":
                city_name = city_obj.uz
            case "en":
                city_name = city_obj.en
            case "ru":
                city_name = city_obj.ru

    ethnicity_obj = await Ethnicity.get_by_id(session, id=profile.ethnicity_id)
    ethnicity_name = get_gendered_field_value(ethnicity_obj, user_language, profile.gender)

    religion_obj = await Religion.get_by_id(session, id=profile.religion_id)
    religion_name = religion_obj.en
    if religion_obj:
        match user_language:
            case "uz":
                religion_name = religion_obj.uz
            case "en":
                religion_name = religion_obj.en
            case "ru":
                religion_name = religion_obj.ru

    # Сборка текста
    profile_text = f"""
{mt.PROFILE_NAME.format(profile.name)}
{mt.PROFILE_AGE.format(profile.age)}
{mt.PROFILE_GENDER.format(gender_map.get(profile.gender, profile.gender))}
{mt.PROFILE_CITY.format(city_name)}
{mt.PROFILE_HEIGHT.format(profile.height)}
{mt.PROFILE_WEIGHT.format(profile.weight)}

{mt.PROFILE_MARITAL_STATUS.format(marital_status_name)}
{mt.PROFILE_HAS_CHILDREN.format(mt.PROFILE_YES if profile.has_children else mt.PROFILE_NO)}"""

    job_text = profile.job if profile.job else "-"
    profile_text += f"""
{mt.PROFILE_EDUCATION.format(education_map.get(profile.education, profile.education))}
{mt.PROFILE_JOB.format(job_text)}
{mt.PROFILE_GOAL.format(goal_map.get(profile.goal, profile.goal))}
{mt.PROFILE_RELIGION.format(religion_name)}"""

    if profile.religious_level:
        profile_text += f"\n{mt.PROFILE_RELIGIOUS_LEVEL.format(religious_level_map.get(profile.religious_level))}"

    profile_text += f"""
{mt.PROFILE_ETHNICITY.format(ethnicity_name)}"""

    about_text = profile.about if profile.about else "-"
    looking_for_text = profile.looking_for if profile.looking_for else "-"

    profile_text += f"""
{mt.PROFILE_ABOUT.format(about_text)}"""
    profile_text += f"""
{mt.PROFILE_LOOKING_FOR.format(looking_for_text)}"""

    return profile_text

async def format_candidate_profile_text(session: AsyncSession, profile: ProfileModel, user_language: str = "ru") -> str:
    """Форматирует профиль для отображения"""

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

    religious_level_map = {
        "low": mt.KB_RELIGIOSITY_LOW,
        "medium": mt.KB_RELIGIOSITY_MEDIUM,
        "high": mt.KB_RELIGIOSITY_HIGH,
        "strict": mt.KB_RELIGIOSITY_STRICT,
        "none": mt.KB_RELIGIOSITY_NONE,
    }

    marital_status_obj = await MaritalStatus.get_by_id(session, id=profile.marital_status_id)
    marital_status_name = get_gendered_field_value(marital_status_obj, user_language, profile.gender)

    city_obj = await City.get_by_id(session, id=profile.city_id)
    city_name = city_obj.en
    if city_obj:
        match user_language:
            case "uz":
                city_name = city_obj.uz
            case "en":
                city_name = city_obj.en
            case "ru":
                city_name = city_obj.ru

    ethnicity_obj = await Ethnicity.get_by_id(session, id=profile.ethnicity_id)
    ethnicity_name = get_gendered_field_value(ethnicity_obj, user_language, profile.gender)

    religion_obj = await Religion.get_by_id(session, id=profile.religion_id)
    religion_name = religion_obj.en
    if religion_obj:
        match user_language:
            case "uz":
                religion_name = religion_obj.uz
            case "en":
                religion_name = religion_obj.en
            case "ru":
                religion_name = religion_obj.ru

    # Сборка текста
    profile_text = f"""
{mt.PROFILE_NAME.format(profile.name)}
{mt.PROFILE_AGE.format(profile.age)}
{mt.PROFILE_CITY.format(city_name)}
{mt.PROFILE_HEIGHT.format(profile.height)}
{mt.PROFILE_WEIGHT.format(profile.weight)}

{mt.PROFILE_MARITAL_STATUS.format(marital_status_name)}
{mt.PROFILE_HAS_CHILDREN.format(mt.PROFILE_YES if profile.has_children else mt.PROFILE_NO)}"""

    job_text = profile.job if profile.job else "-"
    profile_text += f"""
{mt.PROFILE_EDUCATION.format(education_map.get(profile.education, profile.education))}
{mt.PROFILE_JOB.format(job_text)}
{mt.PROFILE_GOAL.format(goal_map.get(profile.goal, profile.goal))}
{mt.PROFILE_RELIGION.format(religion_name)}"""

    if profile.religious_level:
        profile_text += f"\n{mt.PROFILE_RELIGIOUS_LEVEL.format(religious_level_map.get(profile.religious_level))}"

    profile_text += f"""
{mt.PROFILE_ETHNICITY.format(ethnicity_name)}"""
    about_text = profile.about if profile.about else "-"
    looking_for_text = profile.looking_for if profile.looking_for else "-"

    profile_text += f"""
{mt.PROFILE_ABOUT.format(about_text)}"""
    profile_text += f"""
{mt.PROFILE_LOOKING_FOR.format(looking_for_text)}"""

    return profile_text

def get_gendered_field_value(obj, user_language: str, gender: str) -> str:
    if not obj:
        return ""

    lang = user_language.lower()
    gender = gender.lower()

    field_map = {
        ("uz", "male"): "uz_male",
        ("uz", "female"): "uz_female",
        ("ru", "male"): "ru_male",
        ("ru", "female"): "ru_female",
        ("en", "male"): "en_male",
        ("en", "female"): "en_female",
    }

    field_name = field_map.get((lang, gender))

    return getattr(obj, field_name, "")
