import asyncio
from aiogram.exceptions import (
    TelegramBadRequest,
    TelegramForbiddenError,
    TelegramRetryAfter,
    TelegramNotFound,
)
from sqlalchemy.ext.asyncio import AsyncSession

from loader import bot  # содержит bot.username? или тяните из конфига
from utils.logging import logger
from app.text import message_text as mt
from app.business.profile_service import send_profile
from app.keyboards.inline.contact import contact_user_ikb  # если остаётся

async def send_got_chance_alert(
    session: AsyncSession,
    recipient,
    giver,
) -> bool:
    """
    Отправляет получателю профиль дарителя и способ связаться.
    Возвращает True, если что-то было доставлено получателю.
    """
    if not getattr(giver, "profile", None):
        logger.info(f"Даритель {giver.id} без профиля — уведомление не отправлено")
        return False

    # 1) Сообщение "Вам дали шанс"
    try:
        await bot.send_message(
            chat_id=recipient.id,
            text=mt.GOT_CHANCE,  # убедись, что локализация ок
            parse_mode="HTML",
        )
    except TelegramRetryAfter as e:
        await asyncio.sleep(e.retry_after)
        return await send_got_chance_alert(session, recipient, giver)
    except (TelegramForbiddenError, TelegramNotFound) as e:
        # Бот заблокирован или чата нет — можно пометить в БД
        logger.warning(f"Не могу писать {recipient.id}: {e!s}")
        return False
    except TelegramBadRequest as e:
        logger.warning(f"BadRequest при отправке перв. сообщения {recipient.id}: {e!s}")
        # Продолжаем пробовать слать профиль — иногда первое сообщение падает из-за разметки
    except Exception:
        logger.exception("Неожиданная ошибка при отправке перв. сообщения")
        return False

    # 2) Профиль + кнопка (только если есть username)
    reply_markup = None
    if giver.username:
        profile_link = f"https://t.me/{giver.username}"
        # твоя клавиатура, которая делает обычную URL-кнопку
        reply_markup = contact_user_ikb(recipient.language, profile_link)

    try:
        await send_profile(
            session=session,
            chat_id=recipient.id,
            profile=giver.profile,
            user_language=recipient.language,
            reply_markup=reply_markup,
        )

        # Если username нет — отдельной фразой объясняем механику связи
        if not giver.username:
            await bot.send_message(
                chat_id=recipient.id,
                text=(
                    "ℹ️ <b>Информация</b>\n\n"
                    "У этого пользователя приватный профиль.\n"
                    "Пользователь сможет связаться с вами сам."
                ),
                parse_mode="HTML",
                disable_web_page_preview=True,
            )
            await _notify_giver_privacy_block(giver.id)
        return True

    except TelegramBadRequest as e:
        msg = str(e)
        # Замечаем приватные ограничения кнопок/ссылок
        if "BUTTON_USER_PRIVACY_RESTRICTED" in msg:
            # Повторяем без любой URL-кнопки
            try:
                await send_profile(
                    session=session,
                    chat_id=recipient.id,
                    profile=giver.profile,
                    user_language=recipient.language,
                    reply_markup=None,
                )
                await bot.send_message(
                    chat_id=recipient.id,
                    text=(
                        "ℹ️ <b>Информация</b>\n\n"
                        "Из-за настроек приватности нельзя открыть профиль по кнопке.\n"
                        "Пользователь получит уведомление и сможет написать вам сам."
                    ),
                    parse_mode="HTML",
                    disable_web_page_preview=True,
                )
                # Дополнительно можно уведомить дарителя
                await _notify_giver_privacy_block(giver.id)
                return True
            except Exception:
                logger.exception("Повтор без кнопки тоже упал")
                return False
        elif "USER_DEACTIVATED" in msg:
            logger.warning(f"Аккаунт дарителя {giver.id} деактивирован")
            return False
        else:
            logger.warning(f"BadRequest при отправке профиля: {msg}")
            return False
    except (TelegramForbiddenError, TelegramNotFound) as e:
        logger.warning(f"Не могу писать {recipient.id} при отправке профиля: {e!s}")
        return False
    except Exception:
        logger.exception("Неожиданная ошибка при отправке профиля")
        return False


async def _notify_giver_privacy_block(giver_id: int) -> None:
    """Мягко подсказать дарителю про приватность/username."""
    try:
        await bot.send_message(
            chat_id=giver_id,
            text=(
                "⚠️ <b>Внимание</b>\n\n"
                "Из-за настроек приватности с вами нельзя связаться.\n"
                "Совет: установите @username в настройках Telegram."
            ),
            parse_mode="HTML",
        )
    except Exception:
        # Не критично
        logger.debug("Не удалось уведомить дарителя о приватности", exc_info=True)
