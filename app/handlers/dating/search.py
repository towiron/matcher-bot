from aiogram import F, types
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext

from app.business.filter_service import send_filter
from app.business.menu_service import menu
from app.keyboards.default.base import search_kb, search_kb_after_chance, payment_kb
from app.routers import dating_router
from app.states.default import Search
from app.text import message_text as mt
from database.models import UserModel
from database.services import User, Match, Profile, ViewedProfile
from database.services.search import search_profiles
from app.business.profile_service import display_filtered_profile
from aiogram.enums.parse_mode import ParseMode

from loader import _


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


@dating_router.message(
    StateFilter(Search.search),
    F.text.in_((_(mt.KB_NEXT), _(mt.KB_GIVE_CHANCE), _(mt.KB_BACK_TO_SEARCH))),
)
async def _search_profile(
    message: types.Message, state: FSMContext, user: UserModel, session
) -> None:
    """
       Пользователь может взаимодействовать с анкетами, предложенными ботом,
       ставя лайк или дизлайк.
       Также доступна функция жалобы на анкеты, содержащие нежелательный контент.
       Все жалобы отправляются в модераторскую группу, если она указана в настройках.
       """
    data = await state.get_data()
    profile_list = data.get("ids", [])
    another_user = await User.get_with_profile(session, profile_list[0])

    if message.text == _(mt.KB_GIVE_CHANCE):
        try:
            await User.use_one_chance(session, user, another_user.id)
            user_balance = await User.get_chance_balance(user)

            await chance_profile(
                session=session,
                message=message,
                another_user=another_user,
                user_balance=user_balance,
            )
            return
        except ValueError:
            await message.answer("❌ У вас закончились шансы.", reply_markup=payment_kb)
            return

    elif message.text == _(mt.KB_BACK_TO_SEARCH):
        await state.clear()
        await send_filter(session, message.from_user.id, user)
        return

    await next_profile(session, message, profile_list, user, state)

async def chance_profile(
    session,
    message: types.Message,
    another_user: UserModel,
    user_balance: int,
    mail_text: str | None = None,
) -> types.Message:
    is_create = await Match.create(session, message.from_user.id, another_user.id, mail_text)

    if not is_create:
        return await message.answer("Что-то пошло не так", parse_mode=ParseMode.HTML)

    profile_link = (
        f"https://t.me/{another_user.username}"
        if another_user.username
        else f"tg://user?id={another_user.id}"
    )

    text = (
        "💌 Вы дали шанс этому человеку!\n"
        "Посмотри ещё раз анкету — вдруг это начало чего-то особенного?\n"
        f"👉 <a href=\"{profile_link}\">Открыть профиль</a>\n\n"
        f"💎 Вы потратили <b>1</b> шанс, осталось: <b>{user_balance}</b> шанс(ов)."
    )

    return await message.answer(text, parse_mode=ParseMode.HTML, reply_markup=search_kb_after_chance)


async def next_profile(
    session,
    message: types.Message,
    profile_list: list[int],
    user: UserModel,
    state: FSMContext,
):
    if not profile_list:
        await message.answer(mt.EMPTY_PROFILE_SEARCH)
        await state.clear()
        await send_filter(session, message.from_user.id, user)
        return

    shown_user_id = profile_list.pop(0)  # 👈 ID просмотренного профиля

    # ✅ Добавляем запись о просмотре
    await ViewedProfile.get_or_create(
        session,
        viewer_id=user.id,
        viewed_user_id=shown_user_id,
    )

    if profile_list:
        await state.update_data(ids=profile_list)

        profile = await Profile.get(session, profile_list[0])
        await display_filtered_profile(session, user.id, profile, user.language)
    else:
        await message.answer(mt.EMPTY_PROFILE_SEARCH)
        await state.clear()
        await send_filter(session, message.from_user.id, user)