from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware, types
from bot.utils.logging import logger

MAX_PREVIEW_LEN = 80

def _preview(s: str | None, limit: int = MAX_PREVIEW_LEN) -> str:
    if not s:
        return ""
    s = s.replace("\n", "\\n")
    return (s[:limit] + "…") if len(s) > limit else s

class LoggingMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[types.TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: types.TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        user = getattr(event, "from_user", None)
        uid = getattr(user, "id", None)
        uname = getattr(user, "username", None)

        if isinstance(event, types.Message):
            if event.content_type is types.ContentType.WEB_APP_DATA:
                # Ничего из data не логируем (privacy)
                logger.log("MESSAGE", f"{uid} ({uname}): [WebAppData]")
            else:
                text = event.text or event.caption
                logger.log("MESSAGE", f"{uid} ({uname}): {_preview(text)!r}")

        elif isinstance(event, types.CallbackQuery):
            # Короткий превью callback.data, без исходного message и без ct
            logger.log("CALLBACK", f"{uid} ({uname}): {_preview(event.data)!r}")

        return await handler(event, data)
