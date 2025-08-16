from bot.data.config import MODERATOR_GROUP, NEW_USER_ALERT_TO_GROUP
from bot.database.models.user import UserModel
from bot.loader import bot
from bot.utils.logging import logger


async def new_user_alert_to_group(user: UserModel) -> None:
    """Отправляет уведомление в модераторскую группу о новом пользователе"""
    if NEW_USER_ALERT_TO_GROUP and MODERATOR_GROUP:
        try:
            if user.username:
                user_link = f"@{user.username}"
            else:
                user_link = f'<a href="tg://user?id={user.id}">user</a>'

            text = f"New user!\n<code>{user.id}</code> ({user_link})"

            await bot.send_message(
                chat_id=MODERATOR_GROUP,
                text=text,
                parse_mode="HTML"
            )
        except Exception as e:
            logger.error("Сообщение в модераторскую группу не отправлено: %s", e)
