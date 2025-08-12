from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from database.services.base import BaseService
from utils.logging import logger

from ..models.profile import ProfileModel


class Profile(BaseService):
    model = ProfileModel

    @staticmethod
    async def get(session: AsyncSession, id: int):
        """Возвращает профиль пользователя"""
        return await session.get(ProfileModel, id)

    @staticmethod
    async def delete(session: AsyncSession, id: int):
        """Удаляет профиль пользователя"""
        stmt = delete(ProfileModel).where(ProfileModel.id == id)
        await session.execute(stmt)
        await session.commit()
        logger.log("DATABASE", f"{id}: удалил профиль")

    @classmethod
    async def create_or_update(cls, session: AsyncSession, **kwargs):
        """Создаёт профиль пользователя, если профиль есть — обновляет его."""
        user_id = kwargs["id"]  # <- берём реальный id, не builtin

        obj = await cls.get_by_id(session, user_id)
        if obj:
            for key, value in kwargs.items():
                setattr(obj, key, value)
            await session.commit()
            return obj, False

        obj = await cls.create(session, **kwargs)
        # на всякий случай убеждаемся, что id загружен
        if getattr(obj, "id", None) is None:
            await session.flush()
            await session.refresh(obj)

        # Можно логировать и user_id, и profile_id
        logger.log("DATABASE", f"user={user_id}: создал анкету")
        return obj, True

