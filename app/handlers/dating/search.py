from aiogram import F, types
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext

from app.business.menu_service import menu
from app.keyboards.default.base import search_kb
from app.routers import dating_router
from app.states.default import Search
from app.text import message_text as mt
from database.models import UserModel
from database.services import User
from database.services.search import search_profiles
from app.business.profile_service import display_filtered_profile


@dating_router.message(StateFilter(None), F.text == mt.KB_SEARCH_BY_FILTER)
async def _search_command(
    message: types.Message, state: FSMContext, user: UserModel, session
) -> None:
    """Бот подбирает анкеты, соответствующие предпочтениям пользователя, и предлагает их"""
    await message.answer(mt.SEARCH, reply_markup=search_kb)

    if not user.profile:
        await message.answer(mt.FILL_PROFILE_FIRST)
        return

    profile_list = await search_profiles(session, user.profile)

    if profile_list:
        await state.set_state(Search.search)
        await state.update_data(ids=profile_list)

        another_user = await User.get_with_profile(session, profile_list[0])
        if another_user:
            await display_filtered_profile(session, user.id, another_user.profile, user.language)
        else:
            await message.answer(mt.INVALID_PROFILE_SEARCH)
            await menu(message.from_user.id)
    else:
        await message.answer(mt.INVALID_PROFILE_SEARCH)
        await menu(message.from_user.id)

