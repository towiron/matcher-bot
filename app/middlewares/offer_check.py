from functools import wraps
from aiogram import types
from database.models import UserModel

def require_offer_accepted(func):
    """Декоратор для проверки принятия оферты"""
    @wraps(func)
    async def wrapper(message: types.Message, user: UserModel, *args, **kwargs):
        if not user.accepted_offer:
            await message.answer("❗ Вы должны принять оферту перед использованием бота. Введите /start")
            return
        return await func(message, user, *args, **kwargs)
    return wrapper
