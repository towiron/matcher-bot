from sqlalchemy.ext.asyncio import AsyncSession
from bot.data.config import CHANCE_COST
from bot.database.models.user import UserModel
from bot.database.models.balance_entry import BalanceEntryModel
from bot.database.models.enums import EntryKind, Source

class Balance:
    @staticmethod
    async def credit(
        session: AsyncSession,
        user: UserModel,
        delta_chances: int,
        kind: EntryKind,
        source: Source,
        amount_sum: int = 0,
        payload: str | None = None,
        target_id: str | None = None,
    ) -> None:
        """
        Зачисление (бонус/оплата/коррекция+). Увеличивает баланс на delta_chances (>0).
        """
        assert delta_chances > 0, "delta_chances must be positive for credit"
        user.balance_chances += delta_chances
        session.add(BalanceEntryModel(
            user_id=user.id,
            kind=kind,
            source=source,
            delta_chances=delta_chances,
            amount_sum=amount_sum,
            payload=payload,
            target_id=target_id,
        ))
        await session.commit()

    @staticmethod
    async def debit(
        session: AsyncSession,
        user: UserModel,
        delta_chances: int,
        reason: str,
        target_id: str | None = None,
    ) -> None:
        """
        Списание (использование шансов). Уменьшает баланс на delta_chances (>0).
        """
        assert delta_chances > 0, "delta_chances must be positive for debit"
        if user.balance_chances < delta_chances:
            raise ValueError("Недостаточно шансов")

        user.balance_chances -= delta_chances
        session.add(BalanceEntryModel(
            user_id=user.id,
            kind=EntryKind.USAGE,
            source=Source.Internal,
            delta_chances=-delta_chances,
            amount_sum=0,
            payload=reason,
            target_id=target_id,
        ))
        await session.commit()

    @staticmethod
    def sum_to_chances(sum_uzs: int) -> int:
        """Перевод суммы в шансы по текущей цене."""
        return sum_uzs // CHANCE_COST
