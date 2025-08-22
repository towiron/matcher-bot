from aiogram import F
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.enums.parse_mode import ParseMode

from app.business.filter_service import send_filter
from app.business.profile_service import display_filtered_profile
from app.business.dating_service import send_got_chance_alert
from app.keyboards.default.base import search_kb, search_kb_after_chance, payment_kb
from app.keyboards.default.search import build_filter_kb, search_menu_kb
from app.routers import dating_router
from app.states.default import Search
from app.text import message_text as mt
from app.utils.reply_texts import (
    KB_FIND_MATCH_V,
    KB_SEARCH_BY_FILTER_V,
    KB_SEARCH_BY_AI_V,
    KB_GIVE_CHANCE_V,
    KB_NEXT_V,
    KB_BACK_TO_SEARCH_V,
)

from database.models import UserModel
from database.services import User, Match, Profile, ViewedProfile
from database.services.search import search_profiles, search_profiles_by_ai_with_reasons
from sqlalchemy.ext.asyncio import AsyncSession

from utils.logging import logger
from dataclasses import dataclass, asdict
from typing import Dict, List

from aiogram import types

@dating_router.message(StateFilter(None), F.text.in_(KB_FIND_MATCH_V))
async def _search_command(message: types.Message, session: AsyncSession, user: UserModel) -> None:
    # Проверяем, принял ли пользователь оферту
    if not user.filter:
        await message.answer(mt.FILL_FILTER, reply_markup=build_filter_kb(user))
    else:
        await send_filter(session, user.id, user)

@dating_router.message(StateFilter(None), F.text.in_(KB_SEARCH_BY_FILTER_V))
async def _search_command_by_filter(message: types.Message, state: FSMContext, user: UserModel, session: AsyncSession) -> None:
    await start_search_by_filter(message=message, state=state, user=user, session=session)

@dating_router.message(StateFilter(None), F.text.in_(KB_SEARCH_BY_AI_V))
async def _search_by_ai_command(message: types.Message, state: FSMContext, user: UserModel, session: AsyncSession) -> None:
    await start_search_by_ai(message=message, state=state, user=user, session=session)

@dating_router.message(
    StateFilter(Search.search),
    F.text.in_((*KB_NEXT_V, *KB_GIVE_CHANCE_V, *KB_BACK_TO_SEARCH_V)),
)
async def _search_profile(message: types.Message, state: FSMContext, user: UserModel, session: AsyncSession) -> None:
    await handle_search_navigation(message=message, state=state, user=user, session=session)


# ---------- FSM payload ----------

@dataclass
class SearchData:
    ids: List[int]
    mode: str                     # "filter" | "ai"
    ai_reasons: Dict[str, str]    # ключи — строковые id

    @staticmethod
    async def load(state: FSMContext) -> "SearchData":
        data = await state.get_data()
        return SearchData(
            ids=list(data.get("ids", [])),
            mode=data.get("mode", "filter"),
            ai_reasons=dict(data.get("ai_reasons") or {}),
        )

    async def save(self, state: FSMContext) -> None:
        await state.update_data(**asdict(self))


# ---------- guards ----------

async def _ensure_profile_or_ask(message: types.Message, user: UserModel) -> bool:
    if not user.profile:
        await message.answer(mt.FILL_PROFILE_FIRST)
        return False
    return True

async def _ensure_filter_or_show(message: types.Message, session, user: UserModel) -> bool:
    if not user.filter:
        await message.answer(mt.FILL_FILTER, reply_markup=None)  # реплай-кб соберётся в send_filter
        await send_filter(session, user.id, user)
        return False
    return True


# ---------- public API (для хендлеров) ----------

async def start_search_by_filter(
    message: types.Message, state: FSMContext, user: UserModel, session
) -> None:
    """Обычный поиск по фильтрам."""
    # Проверяем, принял ли пользователь оферту
    await message.answer(mt.SEARCH, reply_markup=search_kb())

    if not await _ensure_profile_or_ask(message, user):
        return

    profile_list = await search_profiles(session, user.profile)
    if not profile_list:
        await message.answer(mt.INVALID_PROFILE_SEARCH, reply_markup=search_menu_kb(user=user))
        return

    await state.set_state(Search.search)
    data = SearchData(ids=profile_list, mode="filter", ai_reasons={})
    await data.save(state)

    another_user = await User.get_with_profile(session, profile_list[0])
    if another_user:
        await display_filtered_profile(session, user.id, another_user.profile, user.language)
    else:
        await message.answer(mt.INVALID_PROFILE_SEARCH, reply_markup=search_menu_kb(user=user))


async def start_search_by_ai(
        message: types.Message, state: FSMContext, user: UserModel, session: AsyncSession
) -> None:
    """ИИ-ранжирование + объяснения.
    Проверяем баланс заранее, списываем 3 шанса через User.use_ai_search
    только если нашлись кандидаты.
    """
    await message.answer(mt.SEARCH, reply_markup=search_kb())

    if not await _ensure_profile_or_ask(message, user):
        return

    # 1) Фильтр БД
    profile_list = await search_profiles(session, user.profile)
    if not profile_list:
        await message.answer(mt.INVALID_PROFILE_SEARCH, reply_markup=search_menu_kb(user=user))
        return

    # 2) ИИ-ранжирование
    try:
        ids, reasons = await search_profiles_by_ai_with_reasons(
            session=session,
            user_profile_id=user.profile.id,
            profile_ids=profile_list,
            max_results=5,
            language=user.language,
        )
        logger.log("AI_MATCH_REASONS", f"user={user.id} top={ids} reasons={reasons}")
    except Exception as e:
        logger.log("AI_MATCH_ERROR", f"user={user.id} error: {e}")
        ids, reasons = [], {}

    if not ids:
        # Кандидатов нет — ничего не списываем
        await message.answer(mt.INVALID_PROFILE_SEARCH, reply_markup=search_menu_kb(user=user))
        return

    # 3) Проверяем баланс только после успешного поиска
    balance_now = user.balance_chances
    logger.log("BALANCE_DEBUG", f"user={user.id} balance_now={balance_now} (type: {type(balance_now)})")
    logger.log("BALANCE_DEBUG", f"user={user.id} balance_now < 3 = {balance_now < 3}")

    if balance_now < 3:
        logger.log("BALANCE_DEBUG", f"user={user.id} insufficient_balance: {balance_now} < 3")
        await message.answer(
            text=mt.SMART_SEARCH_BALANCE_ERROR(balance_now),
            reply_markup=payment_kb())
        return

    logger.log("BALANCE_DEBUG", f"user={user.id} balance_check_passed, proceeding to debit")

    # 4) Списываем 3 шанса через User.use_ai_search
    try:
        logger.log("BALANCE_DEBUG", f"user={user.id} calling use_ai_search")
        await User.use_ai_search(session=session, user=user)
        logger.log("BALANCE_DEBIT", f"user={user.id} -3 (smart_search_success via use_ai_search)")
    except ValueError as e:
        logger.log("BALANCE_DEBUG", f"user={user.id} ValueError caught: {e}")
        balance_now = user.balance_chances
        await message.answer(
            text=mt.SMART_SEARCH_BALANCE_ERROR(balance_now),
            reply_markup=payment_kb())
        return
    except Exception as e:
        logger.log("BALANCE_DEBIT_ERROR", f"user={user.id} use_ai_search failed: {e!r}")
        await message.answer(mt.ERR_CHANCES_DEBIT_FAILED, reply_markup=search_menu_kb(user=user))
        return

    logger.log("BALANCE_DEBUG", f"user={user.id} debit_successful, proceeding to show results")

    # 5) Сохраняем состояние и показываем первую анкету
    await state.set_state(Search.search)
    data = SearchData(
        ids=ids,
        mode="ai",
        ai_reasons={str(k): v for k, v in reasons.items()},
    )
    await data.save(state)

    first_id = ids[0]
    another_user = await User.get_with_profile(session, first_id)
    if not another_user:
        await message.answer(mt.INVALID_PROFILE_SEARCH, reply_markup=search_menu_kb(user=user))
        return

    reason_text = data.ai_reasons.get(str(first_id))
    if reason_text:
        await message.answer(text=mt.SMART_SEARCH_MATCH_REASON(reason=reason_text))

    await display_filtered_profile(session, user.id, another_user.profile, user.language)


async def handle_search_navigation(
    message: types.Message, state: FSMContext, user: UserModel, session
) -> None:
    """Обработчик кнопок: Далее / Дать шанс / Назад к поиску / …"""
    data = await SearchData.load(state)
    profile_list = data.ids

    if not profile_list:
        await message.answer(mt.EMPTY_PROFILE_SEARCH)
        await state.clear()
        await send_filter(session, message.from_user.id, user)
        return

    # Ветка "Дать шанс"
    if message.text in KB_GIVE_CHANCE_V:
        another_user = await User.get_with_profile(session, profile_list[0])  # текущий показан
        if not another_user:
            await message.answer(mt.INVALID_PROFILE_SEARCH, reply_markup=search_menu_kb(user=user))
            return
        try:
            await _give_chance(
                session=session,
                message=message,
                user=user,
                another_user=another_user,
            )
            return
        except ValueError:
            await message.answer(mt.ERR_NO_CHANCES_LEFT, reply_markup=payment_kb())
            return

    # Ветка "Назад к настройкам"
    if message.text in KB_BACK_TO_SEARCH_V:
        await state.clear()
        await send_filter(session, message.from_user.id, user)
        return

    # Иначе: «Далее» — показать следующего
    await _show_next_profile(session, message, state, user, data)


async def _give_chance(session, message: types.Message, user: UserModel, another_user: UserModel) -> None:
    # Списываем 1 шанс перед созданием матча
    try:
        await User.use_one_chance(session=session, user=user, target_id=another_user.id)
        logger.log("BALANCE_DEBUG", f"user={user.id} -1 (give_chance via use_one_chance)")
    except ValueError:
        raise ValueError("Недостаточно шансов для дачи шанса")
    except Exception as e:
        logger.log("BALANCE_DEBUG", f"user={user.id} use_one_chance failed: {e!r}")
        await message.answer(mt.ERR_CHANCES_DEBIT_FAILED, parse_mode=ParseMode.HTML)
        return

    # Создаем матч
    is_create = await Match.create(session, message.from_user.id, another_user.id, None)
    if not is_create:
        return

    # Получаем обновленный баланс
    user_balance = await User.get_chance_balance(user)
    profile_link = (
        f"https://t.me/{another_user.username}"
        if another_user.username
        else f"tg://user?id={another_user.id}"
    )

    await message.answer(text=mt.GAVE_CHANCE(profile_link, user_balance), parse_mode=ParseMode.HTML, reply_markup=search_kb_after_chance())

    # Уведомим получателя шанса: отправим ему профиль дарителя и ссылку на контакт
    await send_got_chance_alert(session=session, recipient=another_user, giver=user)


async def _show_next_profile(
    session,
    message: types.Message,
    state: FSMContext,
    user: UserModel,
    data: SearchData,
) -> None:
    ids = data.ids
    if not ids:
        await message.answer(mt.EMPTY_PROFILE_SEARCH)
        await state.clear()
        await send_filter(session, message.from_user.id, user)
        return

    # текущий просмотренный
    shown_user_id = ids.pop(0)

    # логируем просмотр
    await ViewedProfile.get_or_create(session, viewer_id=user.id, viewed_user_id=shown_user_id)

    if not ids:
        # === КОНЕЦ ПАЧКИ ===
        if data.mode == "ai":
            # Проверяем, есть ли ещё кандидаты по обычному фильтру (значит можно снова запустить умный поиск)
            remaining_candidates = await search_profiles(session, user.profile)

            if remaining_candidates:
                await message.answer(text=mt.SMART_SEARCH_EMPTY_REPEAT,
                    reply_markup=search_menu_kb(user=user),
                )
            else:
                await message.answer(
                    text=mt.SMART_SEARCH_EMPTY_FALLBACK,
                    reply_markup=search_menu_kb(user=user),
                )
        else:
            await message.answer(mt.EMPTY_PROFILE_SEARCH)

        await state.clear()
        await send_filter(session, message.from_user.id, user)
        return

    # следующий
    next_id = ids[0]
    data.ids = ids
    await data.save(state)

    # === ВАЖНО: никаких списаний тут! Только показ следующего ===
    if data.mode == "ai":
        reason_text = data.ai_reasons.get(str(next_id))
        if reason_text:
            await message.answer(mt.SMART_SEARCH_MATCH_REASON(reason=reason_text))

    profile = await Profile.get(session, next_id)
    await display_filtered_profile(session, user.id, profile, user.language)
