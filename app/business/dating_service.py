from aiogram.exceptions import TelegramForbiddenError, TelegramBadRequest, TelegramNetworkError

from app.keyboards.inline.archive import check_archive_ikb
from app.text import message_text as mt
from database.models.user import UserModel
from database.services.match import Match
from loader import bot
from utils.logging import logger


async def send_user_like_alert(session, user: UserModel):
    matches = await Match.get_user_matchs(session, user.id)
    text = mt.LIKE_PROFILE(user.language).format(len(matches))
    try:
        await bot.send_message(
            chat_id=user.id,
            text=text,
            reply_markup=check_archive_ikb(user.language),
        )

    except TelegramForbiddenError:
        logger.info(
            f"Пользователю {user.id} @{user.username} не отправлено: бот заблокирован или нет доступа."
        )

    except (TelegramBadRequest, TelegramNetworkError) as e:
        logger.warning(
            f"Не удалось отправить оповещение {user.id} @{user.username}: {e!r}"
        )

    except Exception as e:
        logger.exception(
            f"Неизвестная ошибка при отправке оповещения {user.id} @{user.username}: {e!r}"
        )
