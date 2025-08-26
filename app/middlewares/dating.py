from typing import Any, Callable

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message

from database.models.user import UserStatus
from database.services import User


class DatingMiddleware(BaseMiddleware):
    async def __call__(
        self, handler: Callable, event: Message | CallbackQuery, data: dict
    ) -> Any:
        session = data["session"]
        user, is_create = await User.get_or_create(
            session,
            id=event.from_user.id,
            username=event.from_user.username,
            language=event.from_user.language_code,
        )
        if user.status == UserStatus.Banned:
            return

        if user.profile:
            if not user.profile.is_active:
                return
        data["user"] = user
        return await handler(event, data)
