from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.filter import FilterModel
from database.models.profile import ProfileModel
from database.models.viewed_profile import ViewedProfileModel  # 👈 подключаем модель
from typing import Optional
from utils.logging import logger


async def search_profiles(session: AsyncSession, profile: ProfileModel) -> list[int]:
    # Получаем фильтр пользователя
    filter_obj: Optional[FilterModel] = await session.get(FilterModel, profile.id)
    if not filter_obj:
        return []

    # Ищем противоположный пол
    target_gender = "female" if profile.gender == "male" else "male"

    # 👇 Подзапрос на просмотренные анкеты
    subq = select(ViewedProfileModel.viewed_user_id).where(ViewedProfileModel.viewer_id == profile.id)

    filters = [
        ProfileModel.is_active == True,
        ProfileModel.id != profile.id,
        ProfileModel.gender == target_gender,
        ~ProfileModel.id.in_(subq),  # 👈 исключаем уже просмотренные
    ]

    # Применяем фильтр, только если поле указано
    if filter_obj.city_id is not None:
        filters.append(ProfileModel.city_id == filter_obj.city_id)

    if filter_obj.age_from is not None:
        filters.append(ProfileModel.age >= filter_obj.age_from)
    if filter_obj.age_to is not None:
        filters.append(ProfileModel.age <= filter_obj.age_to)

    if filter_obj.height_from is not None:
        filters.append(ProfileModel.height >= filter_obj.height_from)
    if filter_obj.height_to is not None:
        filters.append(ProfileModel.height <= filter_obj.height_to)

    if filter_obj.weight_from is not None:
        filters.append(ProfileModel.weight >= filter_obj.weight_from)
    if filter_obj.weight_to is not None:
        filters.append(ProfileModel.weight <= filter_obj.weight_to)

    if filter_obj.goal:
        filters.append(ProfileModel.goal == filter_obj.goal)

    if filter_obj.ethnicity_id is not None:
        filters.append(ProfileModel.ethnicity_id == filter_obj.ethnicity_id)

    if filter_obj.has_children is not None:
        filters.append(ProfileModel.has_children == filter_obj.has_children)

    if profile.polygamy is not None:
        filters.append(ProfileModel.polygamy == profile.polygamy)

    if profile.religion_id is not None:
        filters.append(ProfileModel.religion_id == profile.religion_id)

    stmt = select(ProfileModel.id).where(and_(*filters)).order_by(ProfileModel.created_at.desc())
    result = await session.execute(stmt)
    profile_ids = [row[0] for row in result.fetchall()]

    logger.log("DATABASE", f"{profile.id} поиск анкет по фильтру, найдено: {profile_ids}")
    return profile_ids
