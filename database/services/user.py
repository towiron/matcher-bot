from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from data.config import STARTER_CHANCE_COUNT, CHANCE_COST
from database.services.base import BaseService
from utils.logging import logger
from ..models import BalanceTopUpModel, BalanceUsageModel
from ..models.balance_top_up import TopUpSource
from ..models.balance_usage import UsageReason

from ..models.user import UserModel, UserStatus
from .match import Match
from .profile import Profile


class User(BaseService):
    model = UserModel

    @staticmethod
    async def get_with_profile(session: AsyncSession, id: int):
        """Возвращает пользователя и его профиль"""
        result = await session.execute(
            select(UserModel).options(joinedload(UserModel.profile)).where(UserModel.id == id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_with_relations(session: AsyncSession, id: int):
        """Возвращает пользователя с профилем и фильтром"""
        result = await session.execute(
            select(UserModel)
            .options(
                joinedload(UserModel.profile),
                joinedload(UserModel.filter)
            )
            .where(UserModel.id == id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_or_create(
            session: AsyncSession, id: int, username: str = None, language: str = None
    ) -> UserModel:
        if user := await User.get_with_relations(session, id):
            return user, False
        await User.create(session, id=id, username=username, language=language)
        user = await User.get_with_relations(session, id)
        return user, True

    @staticmethod
    async def create(
            session: AsyncSession, id: int, username: str = None, language: str = None
    ) -> UserModel:
        """Создает нового пользователя и записывает стартовые шансы"""
        logger.log("DATABASE", f"New user: {id} (@{username}) {language}")

        user = UserModel(id=id, username=username, language=language)
        session.add(user)

        session.add(BalanceTopUpModel(
            user_id=id,
            amount=STARTER_CHANCE_COUNT,
            paid_sum=CHANCE_COST * STARTER_CHANCE_COUNT,  # 👈 добавляем оплаченные "условные" суммы
            source=TopUpSource.Initial,
            payload="starter_chances"
        ))

        await session.commit()
        return user

    @staticmethod
    async def increment_referral_count(
        session: AsyncSession, user: UserModel, num: int = 1
    ) -> None:
        """Добавляет приведенного реферала к пользователю {inviter_id}"""
        user.referral += num
        await session.commit()
        logger.log("DATABASE", f"{user.id} (@{user.username}): привел нового пользователя")

    async def ban(session: AsyncSession, id: int) -> None:
        """
        Блокирует пользователя:
        - Меняет статус анкеты на неактивный.
        - Меняет статус пользователя на заблокированный.
        - Удаляет все лайки, которые пользователь поставил.
        """
        # Получаем пользователя и его анкету
        user = await User.get_with_profile(session, id)
        if not user:
            logger.log("DATABASE", f"Пользователь с ID {id} не найден.")
            return

        if user.profile:
            await Profile.update(
                session,
                id=id,
                is_active=False,
            )

        await User.update(
            session=session,
            id=id,
            status=UserStatus.Banned,
        )

        # Удаляем все лайки, которые пользователь поставил
        await Match.delete_all_by_sender(session, sender_id=id)

        logger.log("DATABASE", f"Пользователь {id} был заблокирован.")

    @staticmethod
    async def unban(session: AsyncSession, id: int) -> None:
        """
        Разблокирует пользователя:
        - Меняет статус анкеты на активный.
        - Меняет статус пользователя на разблокированный.
        """
        # Получаем пользователя и его анкету
        user = await User.get_with_profile(session, id)
        if not user:
            logger.log("DATABASE", f"Пользователь с ID {id} не найден.")
            return

        if user.profile:
            await Profile.update(
                session,
                id=id,
                is_active=True,
            )

        await User.update(
            session=session,
            id=id,
            status=UserStatus.Banned,
        )

        logger.log("DATABASE", f"Пользователь {id} был разблокирован.")

    @staticmethod
    async def use_one_chance(
            session: AsyncSession,
            user: UserModel,
            target_id: int = None,
    ) -> None:
        """Списывает 1 шанс у пользователя и сохраняет в историю"""
        balance = user.balance - CHANCE_COST

        if balance < 0:
            raise ValueError("Недостаточно шансов для просмотра")

        user.balance -= CHANCE_COST

        session.add(BalanceUsageModel(
            user_id=user.id,
            amount=1,
            reason=UsageReason.ViewProfileManual,
            target_id=str(target_id) if target_id else None
        ))

        await session.commit()

    @staticmethod
    async def get_chance_balance(user: UserModel,) -> int:
        """Возвращает текущий баланс в шансах"""
        chances = user.balance // CHANCE_COST
        return chances


    @staticmethod
    async def add_chances_from_payment(
        session: AsyncSession,
        user: UserModel,
        paid_sum: int,
        source: str = TopUpSource.Click,
        payload: str = None
    ) -> None:
        """
        Пополняет баланс пользователя на указанное количество шансов.
        Сохраняет информацию в таблицу пополнений.
        """
        user.balance += paid_sum
        chance_count = paid_sum // CHANCE_COST

        session.add(BalanceTopUpModel(
            user_id=user.id,
            amount=chance_count,
            paid_sum=paid_sum,
            source=source,
            payload=payload
        ))

        await session.commit()
