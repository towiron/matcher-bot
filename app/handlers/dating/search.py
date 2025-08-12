from aiogram import F, types
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.enums.parse_mode import ParseMode

from app.business.filter_service import send_filter
from app.business.menu_service import menu
from app.business.profile_service import display_filtered_profile
from app.keyboards.default.base import search_kb, search_kb_after_chance, payment_kb
from app.keyboards.default.search import build_filter_kb
from app.routers import dating_router
from app.states.default import Search
from app.text import message_text as mt

from database.models import UserModel
from database.services import User, Match, Profile, ViewedProfile
from database.services.search import search_profiles, search_profiles_by_ai_with_reasons
from sqlalchemy.ext.asyncio import AsyncSession

from utils.logging import logger
from loader import _


@dating_router.message(StateFilter(None), F.text == _(mt.KB_FIND_MATCH))
async def _search_command(message: types.Message, session: AsyncSession, user: UserModel) -> None:
    """Бот подбирает анкеты, соответствующие предпочтениям пользователя, и предлагает их"""
    if not user.filter:
        await message.answer(mt.FILL_FILTER, reply_markup=build_filter_kb(user))
    else:
        await send_filter(session, user.id, user)



@dating_router.message(StateFilter(None), F.text == mt.KB_SEARCH_BY_FILTER)
async def _search_command_by_filter(
    message: types.Message, state: FSMContext, user: UserModel, session
) -> None:
    """Бот подбирает анкеты, соответствующие предпочтениям пользователя, и предлагает их (обычный режим)."""
    await message.answer(mt.SEARCH, reply_markup=search_kb)

    if not user.profile:
        await message.answer(mt.FILL_PROFILE_FIRST)
        return

    profile_list = await search_profiles(session, user.profile)
    if not profile_list:
        await message.answer(mt.INVALID_PROFILE_SEARCH)
        await menu(message.from_user.id)
        return

    await state.set_state(Search.search)
    await state.update_data(
        ids=profile_list,
        mode="filter",      # 👈 явный режим обычного поиска
        ai_reasons=None     # 👈 очищаем причины
    )

    another_user = await User.get_with_profile(session, profile_list[0])
    if another_user:
        await display_filtered_profile(session, user.id, another_user.profile, user.language)
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
    Пользователь взаимодействует с анкетами (лайк/дизлайк/вернуться к настройкам),
    «Далее» показывает следующую анкету согласно текущему режиму (filter/ai).
    """
    data = await state.get_data()
    profile_list = data.get("ids", [])
    if not profile_list:
        await message.answer(mt.EMPTY_PROFILE_SEARCH)
        await state.clear()
        await send_filter(session, message.from_user.id, user)
        return

    another_user = await User.get_with_profile(session, profile_list[0])

    # --- Дать шанс ---
    if message.text == _(mt.KB_GIVE_CHANCE):
        if not another_user:
            await message.answer(mt.INVALID_PROFILE_SEARCH)
            return
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

    # --- Вернуться к настройкам поиска ---
    if message.text == _(mt.KB_BACK_TO_SEARCH):
        await state.clear()
        await send_filter(session, message.from_user.id, user)
        return

    # --- Показать следующую анкету ---
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
    """Показывает следующую анкету и, если режим 'ai', присылает причину."""
    if not profile_list:
        await message.answer(mt.EMPTY_PROFILE_SEARCH)
        await state.clear()
        await send_filter(session, message.from_user.id, user)
        return

    shown_user_id = profile_list.pop(0)  # 👈 текущий просмотренный id

    # ✅ Логируем просмотр
    await ViewedProfile.get_or_create(
        session,
        viewer_id=user.id,
        viewed_user_id=shown_user_id,
    )

    if not profile_list:
        await message.answer(mt.EMPTY_PROFILE_SEARCH)
        await state.clear()
        await send_filter(session, message.from_user.id, user)
        return

    # сохраняем обновлённый список
    await state.update_data(ids=profile_list)

    # режим и причины
    data = await state.get_data()
    mode = data.get("mode", "filter")
    reasons: dict = data.get("ai_reasons") or {}

    next_id = profile_list[0]

    if mode == "ai":
        reason_text = reasons.get(str(next_id)) or reasons.get(next_id)  # 👈 ключ может быть строкой
        if reason_text:
            await message.answer(f"🧠 Почему подходит: {reason_text}")

    profile = await Profile.get(session, next_id)
    await display_filtered_profile(session, user.id, profile, user.language)


@dating_router.message(StateFilter(None), F.text == _(mt.KB_SEARCH_BY_AI))
async def _search_by_ai_command(
    message: types.Message, state: FSMContext, user: UserModel, session
) -> None:
    """ИИ-ранжирование анкет по about/looking_for + объяснения для каждой анкеты."""
    await message.answer(mt.SEARCH, reply_markup=search_kb)

    if not user.profile:
        await message.answer(mt.FILL_PROFILE_FIRST)
        return

    # 1) Грубый фильтр БД
    profile_list = await search_profiles(session, user.profile)
    if not profile_list:
        await message.answer(mt.INVALID_PROFILE_SEARCH)
        await menu(message.from_user.id)
        return

    # 2) ИИ ранжирование + причины
    try:
        ids, reasons = await search_profiles_by_ai_with_reasons(
            session=session,
            user_profile_id=user.profile.id,
            profile_ids=profile_list,
            max_results=5,
            language=user.language,  # если в функции поддержан параметр language
        )
        logger.log("AI_MATCH_REASONS", f"user={user.id} top={ids} reasons={reasons}")
    except Exception as e:
        logger.log("AI_MATCH_ERROR", f"user={user.id} error: {e}")
        ids, reasons = profile_list[:5], {}

    if not ids:
        await message.answer(mt.INVALID_PROFILE_SEARCH)
        await menu(message.from_user.id)
        return

    # 3) Сохраняем режим, ids и причины
    await state.set_state(Search.search)
    await state.update_data(
        ids=ids,
        mode="ai",
        ai_reasons={str(k): v for k, v in reasons.items()}  # 👈 тут
    )

    # 4) Покажем первую анкету и сразу причину
    first_id = ids[0]
    another_user = await User.get_with_profile(session, first_id)
    if another_user:
        reason_text = reasons.get(first_id)
        if reason_text:
            await message.answer(f"🧠 Почему подходит: {reason_text}")
        await display_filtered_profile(session, user.id, another_user.profile, user.language)
    else:
        await message.answer(mt.INVALID_PROFILE_SEARCH)
        await menu(message.from_user.id)
