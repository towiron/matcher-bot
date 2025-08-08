from typing import Any, Callable, Optional, Tuple
from datetime import date, timedelta, timezone
import pytz

from aiogram import BaseMiddleware
from aiogram.types import Update
from sqlalchemy.ext.asyncio import AsyncSession

from data.config import CHANCE_COST
from database.models import BalanceTopUpModel
from database.models.balance_top_up import TopUpSource
from database.models.user import UserModel, UserStatus
from database.services import User

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
    """
    Достаёт (user_id, chat_id, username, language) из Update.
    Для остальных типов апдейтов возвращает (None, None, None, None).
    """
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
    - В любой другой день: при первой активности за сутки — daily_streak (+1 или =1) и выдаём 1 шанс.
    - Идёмпотентность за счёт сравнения last_active_date с сегодняшней датой.
    - Уведомляем пользователя, только если бонус реально выдан.
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
        if user.profile and not user.profile.is_active:
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
            text = (
                f"🎁 Вы получили ежедневный бонус: 1 шанс!\n"
                f"🔥 Ваш текущий стрик: {user.daily_streak} дн."
            )

            try:
                await bot.send_message(chat_id, text)
            except Exception:
                # логировать по желанию, но пайплайн не роняем
                pass

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

        # ежедневный бонус: +1 шанс (в суммах = CHANCE_COST)
        add_sum = CHANCE_COST
        user.balance += add_sum
        session.add(BalanceTopUpModel(
            user_id=user.id,
            amount=1,                  # 1 шанс
            paid_sum=add_sum,          # на твоей модели баланс в суммах
            source=TopUpSource.Initial,  # можешь заменить на TopUpSource.Internal, если есть
            payload="bonus:daily",
        ))

        await session.commit()
        return True
