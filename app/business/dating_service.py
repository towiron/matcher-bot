from app.keyboards.inline.archive import check_archive_ikb
from app.text import message_text as mt
from database.models.user import UserModel
from database.services.match import Match
from loader import bot
from utils.logging import logger
from sqlalchemy.ext.asyncio import AsyncSession
from app.business.profile_service import send_profile
from app.keyboards.inline.contact import contact_user_ikb


async def send_got_chance_alert(session: AsyncSession, recipient: UserModel, giver: UserModel) -> None:
    """Отправляет получателю шансa профиль дарителя и ссылку на него."""
    try:
        if giver.profile:
            if giver.username:
                profile_link = f"https://t.me/{giver.username}"
            else:
                profile_link = f"tg://user?id={giver.id}"
            await bot.send_message(chat_id=recipient.id, text=mt.GOT_CHANCE)
            await send_profile(
                session,
                recipient.id,
                giver.profile,
                recipient.language,
                reply_markup=contact_user_ikb(recipient.language, profile_link),
            )
    except Exception as e:
        logger.info(
            f"Пользователю {recipient.id} @{recipient.username}: оповещение о шансе не отправлено, {e}"
        )
