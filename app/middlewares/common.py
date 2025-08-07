from typing import Any, Callable

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message

from app.business.alert_service import new_user_alert_to_group
from database.models.user import UserStatus
from database.services import User
from database.services.profile import Profile
from utils.base62 import decode_base62


class CommonMiddleware(BaseMiddleware):
    async def __call__(
        self, handler: Callable, message: Message | CallbackQuery, data: dict
    ) -> Any:
        session = data["session"]

        user, is_create = await User.get_or_create(
            session,
            id=message.from_user.id,
            username=message.from_user.username,
            language=message.from_user.language_code,
        )

        if user.status == UserStatus.Banned:
            return  # ничего не делаем для заблокированных

        # 💡 Добавляем пользователя в data
        data["user"] = user

        # 💥 Проверка принятия оферты
        is_start_command = isinstance(message, Message) and message.text and message.text.startswith("/start")
        is_offer_callback = isinstance(message, CallbackQuery) and message.data and message.data.startswith("offer_")

        if not user.accepted_offer and not (is_start_command or is_offer_callback):
            msg = message.message if isinstance(message, CallbackQuery) else message
            await msg.answer("❗ Вы должны принять оферту перед использованием бота. Введите /start")
            return  # прерываем цепочку

        # 📦 Обработка новых пользователей и рефералов
        if isinstance(message, Message):
            if is_create:
                if inviter_code := getattr(data.get("command"), "args", None):
                    if inviter := await User.get_by_id(session, decode_base62(inviter_code)):
                        await User.increment_referral_count(session, inviter)
                await new_user_alert_to_group(user)

            # Автоматически активируем анкету, если она была отключена
            if user.profile and not user.profile.is_active:
                await Profile.update(
                    session=session,
                    id=user.id,
                    is_active=True,
                )

        return await handler(message, data)
