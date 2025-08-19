from typing import Any, Callable, List
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery, TelegramObject

from loader import _
from app.text import message_text as mt


class OfferCheckMiddleware(BaseMiddleware):
    def __init__(self, allowed_callbacks: List[str] = None, allowed_commands: List[str] = None):
        """
        Middleware для проверки принятия оферты пользователем

        Args:
            allowed_callbacks: Дополнительные разрешенные callback_data префиксы
            allowed_commands: Дополнительные разрешенные команды
        """
        self.allowed_callbacks = allowed_callbacks or []
        self.allowed_commands = allowed_commands or []
        super().__init__()

    async def __call__(self, handler: Callable, event: TelegramObject, data: dict) -> Any:
        user = data.get("user")

        if not user:
            # Если пользователя нет в data, значит CommonMiddleware не отработал
            # Это не должно происходить, но на всякий случай продолжаем
            return await handler(event, data)

        # Если пользователь уже принял оферту, пропускаем проверку
        if user.accepted_offer:
            return await handler(event, data)

        # ----- Разрешённые действия до принятия оферты -----

        # Базовые разрешенные команды
        is_start_command = isinstance(event, Message) and (event.text or "").startswith("/start")
        is_lang_command = isinstance(event, Message) and (event.text or "") in ("/lang", "/language")
        is_help_command = isinstance(event, Message) and (event.text or "").lower() in ("/help", "help", "помощь")

        # Базовые разрешенные коллбэки
        is_offer_callback = isinstance(event, CallbackQuery) and (event.data or "").startswith("offer_")
        is_lang_callback = isinstance(event, CallbackQuery) and (event.data or "").startswith("lang:")

        # Дополнительные разрешенные команды (переданные в конструктор)
        is_custom_command = isinstance(event, Message) and (event.text or "") in self.allowed_commands

        # Дополнительные разрешенные коллбэки (переданные в конструктор)
        is_custom_callback = isinstance(event, CallbackQuery) and any(
            (event.data or "").startswith(prefix) for prefix in self.allowed_callbacks
        )

        is_allowed_before_offer = any((
            is_start_command,
            is_lang_command,
            is_help_command,
            is_offer_callback,
            is_lang_callback,
            is_custom_command,
            is_custom_callback,
        ))

        # Если действие не разрешено до принятия оферты, блокируем
        if not is_allowed_before_offer:
            if isinstance(event, CallbackQuery):
                await event.answer()  # убрать «часики»
                msg = event.message
                if msg:
                    await msg.answer(_(mt.OFFER_REQUIRED))
            else:
                await event.answer(_(mt.OFFER_REQUIRED))
            return  # Прерываем выполнение

        # Переходим дальше
        return await handler(event, data)