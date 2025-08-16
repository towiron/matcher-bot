from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from bot.data.config import STARTER_CHANCE_COUNT, CHANCE_COST
from bot.database.services.base import BaseService
from bot.utils.logging import logger

from ..models.user import UserModel, UserStatus
from .match import Match
from .profile import Profile

# ⚙️ новый леджер
from bot.database.services.balance import Balance
from bot.database.models.enums import EntryKind, Source


class User(BaseService):
    model = UserModel

    # ---------- GETTERS ----------

    @staticmethod
    async def get_with_profile(session: AsyncSession, id: int) -> Optional[UserModel]:
        """Возвращает пользователя и его профиль"""
        result = await session.execute(
            select(UserModel)
            .options(joinedload(UserModel.profile))
            .where(UserModel.id == id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_with_relations(session: AsyncSession, id: int) -> Optional[UserModel]:
        """Возвращает пользователя с профилем и фильтром"""
        result = await session.execute(
            select(UserModel)
            .options(
                joinedload(UserModel.profile),
                joinedload(UserModel.filter),
            )
            .where(UserModel.id == id)
        )
        return result.scalar_one_or_none()

    # ---------- CREATE / UPSERT ----------

    @staticmethod
    async def get_or_create(
        session: AsyncSession, id: int, username: str | None = None, language: str | None = None
    ) -> tuple[Optional[UserModel], bool]:
        if user := await User.get_with_relations(session, id):
            return user, False
        user = await User.create(session, id=id, username=username, language=language)
        return user, True

    @staticmethod
    async def create(
        session: AsyncSession, id: int, username: str | None = None, language: str | None = None
    ) -> UserModel:
        """Создаёт пользователя и выдаёт стартовые шансы через леджер."""
        logger.log("DATABASE", f"New user: {id} (@{username}) {language}")

        user = UserModel(id=id, username=username, language=language)
        session.add(user)
        await session.flush()  # получить user.id для леджера

        # Стартовые шансы как бонус (Initial)
        if STARTER_CHANCE_COUNT and STARTER_CHANCE_COUNT > 0:
            await Balance.credit(
                session=session,
                user=user,
                delta_chances=STARTER_CHANCE_COUNT,
                kind=EntryKind.BONUS,
                source=Source.Initial,
                amount_sum=STARTER_CHANCE_COUNT * CHANCE_COST,  # опционально для отчётов
                payload="starter_chances",
            )

        # commit уже был внутри Balance.credit
        return user

    # ---------- MODERATE ----------

    @staticmethod
    async def ban(session: AsyncSession, id: int) -> None:
        """
        Блокирует пользователя:
        - Меняет статус анкеты на неактивный.
        - Меняет статус пользователя на заблокированный.
        - Удаляет все лайки, которые пользователь поставил.
        """
        user = await User.get_with_profile(session, id)
        if not user:
            logger.log("DATABASE", f"Пользователь с ID {id} не найден.")
            return

        if user.profile:
            await Profile.update(session, id=id, is_active=False)

        await User.update(session=session, id=id, status=int(UserStatus.Banned))
        await Match.delete_all_by_sender(session, sender_id=id)

        logger.log("DATABASE", f"Пользователь {id} был заблокирован.")

    @staticmethod
    async def unban(session: AsyncSession, id: int) -> None:
        """
        Разблокирует пользователя:
        - Меняет статус анкеты на активный.
        - Меняет статус пользователя на обычный.
        """
        user = await User.get_with_profile(session, id)
        if not user:
            logger.log("DATABASE", f"Пользователь с ID {id} не найден.")
            return

        if user.profile:
            await Profile.update(session, id=id, is_active=True)

        await User.update(session=session, id=id, status=int(UserStatus.User))
        logger.log("DATABASE", f"Пользователь {id} был разблокирован.")

    # ---------- BALANCE OPS (совместимо со старым API) ----------

    @staticmethod
    async def use_one_chance(
        session: AsyncSession, user: UserModel, target_id: int | None = None
    ) -> None:
        """Списывает 1 шанс (через леджер)."""
        await Balance.debit(
            session=session,
            user=user,
            delta_chances=1,
            reason="view_profile_manual",
            target_id=str(target_id) if target_id else None,
        )


    @staticmethod
    async def use_ai_search(
            session: AsyncSession, user: UserModel, target_id: int | None = None
    ) -> None:
        """Списывает 3 шанса (через леджер)."""
        await Balance.debit(
            session=session,
            user=user,
            delta_chances=3,
            reason="ai_search",
            target_id=str(target_id) if target_id else None,
        )

    @staticmethod
    async def get_chance_balance(user: UserModel) -> int:
        """Возвращает текущий баланс в шансах (кеш на пользователе)."""
        return int(user.balance_chances)

    # -- deprecated: заменить на вызовы Balance.credit в новом коде
    @staticmethod
    async def add_chances_from_payment(
        session: AsyncSession,
        user: UserModel,
        paid_sum: int,
        source: str = "click",
        payload: str | None = None,
    ) -> None:
        """
        [Совместимость] Пополняет баланс на оплаченные шансы как TOP_UP.
        Лучше вызывать Balance.credit напрямую из хендлера оплаты.
        """
        # конвертим строку source -> Source enum, по умолчанию Click
        src = {
            "click": Source.Click,
            "payme": Source.Payme,
            "uzum": Source.Uzum,
            "internal": Source.Internal,
            "initial": Source.Initial,
        }.get(source, Source.Click)

        paid_chances = Balance.sum_to_chances(paid_sum)
        if paid_chances <= 0:
            return

        await Balance.credit(
            session=session,
            user=user,
            delta_chances=paid_chances,
            kind=EntryKind.TOP_UP,
            source=src,
            amount_sum=paid_sum,
            payload=payload,
        )

    # ---------- MISC ----------

    @staticmethod
    async def update_offer_accepted(
        session: AsyncSession, user_id: int, value: bool = True
    ) -> None:
        """Обновляет флаг принятия пользовательской оферты."""
        await session.execute(
            update(UserModel)
            .where(UserModel.id == user_id)
            .values(accepted_offer=value)
        )
        await session.commit()
        logger.log("DATABASE", f"Пользователь {user_id} {'принял' if value else 'отклонил'} оферту")
