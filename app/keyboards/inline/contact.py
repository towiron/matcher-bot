from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from loader import _


def contact_user_ikb(language: str, profile_link: str) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(
        resize_keyboard=True,
        inline_keyboard=[
            [InlineKeyboardButton(text=_("Открыть профиль", locale=language), url=profile_link)],
        ],
    )
    return ikb


