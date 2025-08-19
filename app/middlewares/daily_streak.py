from typing import Any, Callable, Optional, Tuple
from datetime import date, timedelta, timezone
import pytz

from aiogram import BaseMiddleware
from aiogram.types import Update
from sqlalchemy.ext.asyncio import AsyncSession

from data.config import CHANCE_COST
from database.models.user import UserModel, UserStatus
from database.services import User

from database.services.balance import Balance
from database.models.enums import EntryKind, Source

from loader import _
from app.text import message_text as mt

_TZ = pytz.timezone("Asia/Tashkent")


def _today_tashkent() -> date:
    from datetime import datetime
    return datetime.now(_TZ).date()


def _to_tashkent_date(dt) -> Optional[date]:
    """Приводит datetime к локальной (Asia/Tashkent) дате. Если tz не задан — считаем UTC."""
    if dt is None:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(_TZ).date()


def _extract_user_and_chat(update: Update) -> Tuple[Optional[int], Optional[int], Optional[str], Optional[str]]:
    """Достаёт (user_id, chat_id, username, language) из Update."""
    if update.message:
        u = update.message.from_user
        return (
            (u.id if u else None),
            update.message.chat.id,
            (u.username if u else None),
            (u.language_code if u else None),
        )
    if update.callback_query:
        u = update.callback_query.from_user
        chat_id = update.callback_query.message.chat.id if update.callback_query.message else None
        return (
            (u.id if u else None),
            chat_id,
            (u.username if u else None),
            (u.language_code if u else None),
        )
    return (None, None, None, None)


class DailyStreakMiddleware(BaseMiddleware):
    """
    Правила:
    - День регистрации: бонус НЕ даём, но отмечаем активность (last_active_date=today) и ставим daily_streak=1.
    - В другие дни: при первой активности за сутки — стрик (+1/1) и выдаём +1 шанс через леджер.
    - Уведомляем пользователя только если бонус реально выдан.
    """

    async def __call__(self, handler: Callable, event: Update, data: dict) -> Any:
        session: AsyncSession = data["session"]
        bot = data["bot"]

        user_id, chat_id, username, language = _extract_user_and_chat(event)
        if not user_id:
            return await handler(event, data)

        # 1) получаем/создаём пользователя
        user, is_create = await User.get_or_create(
            session,
            id=user_id,
            username=username,
            language=language,
        )

        # 2) фильтры
        if user.status == UserStatus.Banned:
            return
        
        # Исправление: безопасная проверка активности профиля
        # Избегаем проблем с ленивой загрузкой, делая прямой запрос к БД
        from sqlalchemy import select
        from database.models.profile import ProfileModel
        
        profile_result = await session.execute(
            select(ProfileModel.is_active).where(ProfileModel.id == user.id)
        )
        profile_active = profile_result.scalar_one_or_none()
        
        if profile_active is False:  # Явно проверяем False, не None
            return

        today = _today_tashkent()

        # 3) День регистрации: НЕ даём бонус, но фиксируем активность и стартуем стрик = 1
        created_local = _to_tashkent_date(getattr(user, "created_at", None))
        if is_create or (created_local == today):
            if user.last_active_date != today:
                user.daily_streak = 1
                user.last_active_date = today
                await session.commit()
            data["user"] = user
            return await handler(event, data)

        # 4) Обычный день: попробуем выдать ежедневный бонус (только при первой активности за день)
        got_bonus = await self._touch_today(session, user, today)

        # 5) уведомление, если бонус реально выдан
        if got_bonus and chat_id:
            try:
                await bot.send_message(chat_id, _(mt.DAILY_BONUS(streak=user.daily_streak)))
            except Exception:
                pass  # не роняем пайплайн

        data["user"] = user
        return await handler(event, data)

    async def _touch_today(self, session: AsyncSession, user: UserModel, today: date) -> bool:
        """Возвращает True, если сегодня первый раз и бонус выдан."""
        if user.last_active_date == today:
            return False

        # стрик
        if user.last_active_date is None:
            user.daily_streak = 1
        elif user.last_active_date == (today - timedelta(days=1)):
            user.daily_streak += 1
        else:
            user.daily_streak = 1

        user.last_active_date = today
        await session.flush()

        # ежедневный бонус: +1 шанс через леджер (BONUS/Internal)
        await Balance.credit(
            session=session,
            user=user,
            delta_chances=1,
            kind=EntryKind.BONUS,
            source=Source.Internal,
            amount_sum=CHANCE_COST,   # опционально для отчётов; можно 0
            payload="bonus:daily",
        )

        # commit сделает Balance.credit
        return True
