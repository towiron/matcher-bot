from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.services.base import BaseService
from bot.utils.logging import logger

from ..models.filter import FilterModel


class Filter(BaseService):
    model = FilterModel

    @staticmethod
    async def get(session: AsyncSession, id: int):
        """Возвращает фильтр пользователя"""
        return await session.get(FilterModel, id)

    @staticmethod
    async def delete(session: AsyncSession, id: int):
        """Удаляет фильтр пользователя"""
        stmt = delete(FilterModel).where(FilterModel.id == id)
        await session.execute(stmt)
        await session.commit()
        logger.log("DATABASE", f"{id}: удалил фильтр")

    @classmethod
    async def create_or_update(cls, session: AsyncSession, **kwargs):
        """Создает фильтр пользователя, если фильтр есть - обновляет его"""
        obj = await cls.get_by_id(session, kwargs["id"])
        if obj:
            for key, value in kwargs.items():
                setattr(obj, key, value)
            await session.commit()
            return obj, False
        obj = await cls.create(session, **kwargs)
        logger.log("DATABASE", f"{id}: создал фильтр")
        return obj, True