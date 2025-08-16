from bot.app.keyboards.default.base import menu_kb
from bot.app.text import message_text as mt
from bot.loader import bot


async def menu(chat_id: int) -> None:
    """Отправляет меню пользователю"""
    await bot.send_message(
        chat_id=chat_id,
        text=mt.MENU,
        reply_markup=menu_kb,
    )
