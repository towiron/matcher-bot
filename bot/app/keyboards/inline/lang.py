from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.app.filters.kb_filter import LangCallback
from bot.loader import i18n

language_dict = {
    "ru": "🇷🇺 Русский",
    # "uz": "🇺🇿 O'zbek",
    # "en": "🇬🇧 English",
}


def lang_ikb():
    builder = InlineKeyboardBuilder()
    [
        builder.button(text=language_dict[lang], callback_data=LangCallback(lang=lang))
        for lang in i18n.available_locales
    ]
    builder.adjust(3)

    return builder.as_markup()
