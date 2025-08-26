from typing import Any, Callable

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message
from sqlalchemy import select

from app.business.alert_service import new_user_alert_to_group
from database.models.user import UserStatus
from database.models.profile import ProfileModel
from database.services import User
from database.services.profile import Profile
from loader import _
from app.text import message_text as mt



class CommonMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable, event: Message | CallbackQuery, data: dict) -> Any:
        session = data["session"]

        user, is_create = await User.get_or_create(
            session,
            id=event.from_user.id,
            username=event.from_user.username,
            language=event.from_user.language_code,
        )

        if user.status == UserStatus.Banned:
            return  # ничего не делаем для заблокированных

        data["user"] = user

        # Проверка принятия оферты
        is_start_command = isinstance(event, Message) and event.text and event.text.startswith("/start")
        is_offer_callback = isinstance(event, CallbackQuery) and event.data and event.data.startswith("offer_")
        is_lang_callback = isinstance(event, CallbackQuery) and event.data and event.data.startswith("lang:")
        is_lang_command = isinstance(event, Message) and event.text and event.text in ["/lang", "/language"]

        # Добавляем проверку на команды помощи
        is_help_command = isinstance(event, Message) and event.text and event.text in ["/help", "Помощь"]

        if not user.accepted_offer and not (is_start_command or is_offer_callback or is_lang_callback or is_lang_command or is_help_command):
            msg = event.message if isinstance(event, CallbackQuery) else event
            await msg.answer(_(mt.OFFER_REQUIRED))
            return

        # Новые пользователи
        if isinstance(event, Message):
            if is_create:
                await new_user_alert_to_group(user)

            # Авто-активация анкеты без lazy-load
            is_active = await session.scalar(
                select(ProfileModel.is_active).where(ProfileModel.id == user.id)
            )
            if is_active is False:
                await Profile.update(session=session, id=user.id, is_active=True)

        return await handler(event, data)