from typing import Tuple

from loader import i18n


# Supported locales for ReplyKeyboard texts
SUPPORTED_LOCALES: Tuple[str, ...] = ("ru", "uz")


def variants(source_text: str) -> Tuple[str, ...]:
    """Return translated variants of a source text for all supported locales.

    We pass locale explicitly to avoid depending on middleware context.
    """
    return tuple(i18n.gettext(source_text, locale=loc) for loc in SUPPORTED_LOCALES)


# Base source strings used in ReplyKeyboards
KB_FIND_MATCH_V = variants("🔍 Найти пару")
KB_MY_PROFILE_V = variants("👤 Мой профиль")
KB_BACK_V = variants("↩️ Назад")
KB_DISABLE_PROFILE_V = variants("❌ Я больше не хочу никого искать")
KB_GIVE_CHANCE_V = variants("Шанс (1 💎)")
KB_NEXT_V = variants("Следующий")
KB_BUY_CHANCES_V = variants("💎 Пополнить шансы")
KB_BACK_TO_SEARCH_V = variants("Меню поиска")
KB_SEARCH_BY_FILTER_V = variants("🔍 Поиск по фильтру")
KB_SEARCH_BY_AI_V = variants("🧠 Умный поиск (3 💎)")


