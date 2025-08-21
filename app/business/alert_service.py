from data.config import MODERATOR_GROUP, NEW_USER_ALERT_TO_GROUP
from database.models.user import UserModel
from loader import bot
from utils.logging import logger


async def new_user_alert_to_group(user: UserModel) -> None:
    """Отправляет уведомление в модераторскую группу о новом пользователе"""
    if NEW_USER_ALERT_TO_GROUP and MODERATOR_GROUP:
        try:
            if user.username:
                user_link = f"@{user.username}"
            else:
                user_link = f'<a href="tg://user?id={user.id}">user</a>'

            text = f"<b>🆕 Новый пользователь</b>\nID: <code>{user.id}</code>\nСсылка: ({user_link})\n#new"

            await bot.send_message(
                chat_id=MODERATOR_GROUP,
                text=text,
            )
        except Exception as e:
            logger.error("Сообщение в модераторскую группу не отправлено: {}", e)
