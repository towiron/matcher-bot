from aiogram import F
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.enums.parse_mode import ParseMode

from app.business.filter_service import send_filter
from app.business.profile_service import display_filtered_profile, update_user_username_from_telegram
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
async def _search_command(message: types.Message, session: AsyncSession, user: UserModel, state: FSMContext) -> None:
    # Проверяем, принял ли пользователь оферту
    if not user.filter:
        await message.answer(mt.FILL_FILTER, reply_markup=build_filter_kb(user))
    else:
        # Сначала проверяем, есть ли приостановленный поиск
        search_resumed = await check_and_resume_paused_search(message, state, user, session)
        if not search_resumed:
            # Если нет приостановленного поиска, показываем обычное меню поиска
            await send_filter(session, user.id, user)

@dating_router.message(StateFilter(None), F.text.in_(KB_SEARCH_BY_FILTER_V))
async def _search_command_by_filter(message: types.Message, state: FSMContext, user: UserModel, session: AsyncSession) -> None:
    # Сначала проверяем, есть ли приостановленный поиск
    search_resumed = await check_and_resume_paused_search(message, state, user, session)
    if not search_resumed:
        # Если нет приостановленного поиска, запускаем новый поиск
        await start_search_by_filter(message=message, state=state, user=user, session=session)

@dating_router.message(StateFilter(None), F.text.in_(KB_SEARCH_BY_AI_V))
async def _search_by_ai_command(message: types.Message, state: FSMContext, user: UserModel, session: AsyncSession) -> None:
    # Сначала проверяем, есть ли приостановленный поиск
    search_resumed = await check_and_resume_paused_search(message, state, user, session)
    if not search_resumed:
        # Если нет приостановленного поиска, проверяем поля профиля
        if not await _ensure_ai_search_fields(message, user):
            return
        # Если поля заполнены, запускаем новый поиск
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
    paused_for_payment: bool = False  # флаг, что поиск приостановлен для оплаты

    @staticmethod
    async def load(state: FSMContext) -> "SearchData":
        data = await state.get_data()
        return SearchData(
            ids=list(data.get("ids", [])),
            mode=data.get("mode", "filter"),
            ai_reasons=dict(data.get("ai_reasons") or {}),
            paused_for_payment=data.get("paused_for_payment", False),
        )

    async def save(self, state: FSMContext) -> None:
        await state.update_data(**asdict(self))


# ---------- guards ----------

async def _ensure_profile_or_ask(message: types.Message, user: UserModel) -> bool:
    if not user.profile:
        await message.answer(mt.FILL_PROFILE_FIRST)
        return False
    return True

async def _ensure_filter_or_show(message: types.Message, session: AsyncSession, user: UserModel) -> bool:
    if not user.filter:
        await message.answer(mt.FILL_FILTER, reply_markup=None)  # реплай-кб соберётся в send_filter
        await send_filter(session, user.id, user)
        return False
    return True

async def _ensure_ai_search_fields(message: types.Message, user: UserModel) -> bool:
    """Проверяет, заполнены ли поля профиля для умного поиска."""
    if not user.profile:
        await message.answer(mt.FILL_PROFILE_FIRST)
        return False
    
    # Проверяем критически важные поля для умного поиска
    missing_fields = []
    short_fields = []
    
    if not user.profile.about or user.profile.about.strip() == "":
        missing_fields.append("О себе")
    elif len(user.profile.about.strip()) < 20:
        short_fields.append("О себе (минимум 20 символов)")
    
    if not user.profile.looking_for or user.profile.looking_for.strip() == "":
        missing_fields.append("Кого ищете")
    elif len(user.profile.looking_for.strip()) < 20:
        short_fields.append("Кого ищете (минимум 20 символов)")
    
    if missing_fields or short_fields:
        all_fields = missing_fields + short_fields
        fields_text = ", ".join(all_fields)
        
        if missing_fields:
            message_text = (
                f"❌ Для использования умного поиска необходимо заполнить следующие поля профиля:\n\n"
                f"📝 {fields_text}\n\n"
            )
        else:
            message_text = (
                f"⚠️ Для качественного умного поиска рекомендуется расширить следующие поля профиля:\n\n"
                f"📝 {fields_text}\n\n"
            )
        
        message_text += (
            "💡 Умный поиск анализирует ваши интересы и предпочтения, "
            "поэтому важно подробно описать себя и кого вы ищете.\n\n"
            "Пожалуйста, дополните свой профиль и попробуйте снова."
        )
        
        await message.answer(message_text, reply_markup=search_menu_kb(user=user))
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
        # Обновляем username пользователя из Telegram перед показом профиля
        await update_user_username_from_telegram(session, profile_list[0])
        
        await display_filtered_profile(session, user.id, another_user.profile, user.language, user.id)
    else:
        await message.answer(mt.INVALID_PROFILE_SEARCH, reply_markup=search_menu_kb(user=user))


async def start_search_by_ai(
        message: types.Message, state: FSMContext, user: UserModel, session: AsyncSession
) -> None:
    """ИИ-ранжирование + объяснения.
    1) Проверяем баланс перед ИИ-запросом
    2) Делаем ИИ-поиск только если есть шансы
    3) Списываем 3 шанса только если ИИ нашел кандидатов
    """
    await message.answer(mt.SEARCH, reply_markup=search_kb())

    if not await _ensure_profile_or_ask(message, user):
        return

    # 1) Проверяем баланс ПЕРЕД любыми операциями
    balance_now = user.balance_chances
    logger.log("BALANCE_DEBUG", f"user={user.id} balance_now={balance_now} (type: {type(balance_now)})")
    
    if balance_now < 3:
        logger.log("BALANCE_DEBUG", f"user={user.id} insufficient_balance: {balance_now} < 3")
        await message.answer(
            text=mt.SMART_SEARCH_BALANCE_ERROR(balance_now),
            reply_markup=payment_kb())
        return

    # 2) Фильтр БД
    profile_list = await search_profiles(session, user.profile)
    if not profile_list:
        await message.answer(mt.INVALID_PROFILE_SEARCH, reply_markup=search_menu_kb(user=user))
        return

    # 3) ИИ-ранжирование (только если есть баланс)
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
        # ИИ не нашел подходящих кандидатов — ничего не списываем
        await message.answer(
            "🤖 Умный поиск не смог найти подходящих кандидатов на данный момент.\n\n"
            "💡 Попробуйте:\n"
            "• Обновить описание профиля\n"
            "• Расширить критерии поиска\n"
            "• Попробовать обычный поиск",
            reply_markup=search_menu_kb(user=user)
        )
        return

    # 4) Списываем 3 шанса через User.use_ai_search
    logger.log("BALANCE_DEBUG", f"user={user.id} balance_check_passed, proceeding to debit")
    try:
        logger.log("BALANCE_DEBUG", f"user={user.id} calling use_ai_search")
        await User.use_ai_search(session=session, user=user)
        await session.refresh(user)  # Обновляем баланс пользователя
        logger.log("BALANCE_DEBIT", f"user={user.id} -3 (smart_search_success via use_ai_search)")
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

    # Обновляем username пользователя из Telegram перед показом профиля
    await update_user_username_from_telegram(session, first_id)

    reason_text = data.ai_reasons.get(str(first_id))
    if reason_text:
        await message.answer(text=mt.SMART_SEARCH_MATCH_REASON(reason=reason_text))

    await display_filtered_profile(session, user.id, another_user.profile, user.language, user.id)


async def handle_search_navigation(
    message: types.Message, state: FSMContext, user: UserModel, session
) -> None:
    """Обработчик кнопок: Далее / Дать шанс / Назад к поиску / …"""
    data = await SearchData.load(state)
    profile_list = data.ids

    if not profile_list:
        # Проверяем, есть ли профили по текущему фильтру
        remaining_profiles = await search_profiles(session, user.profile)
        if remaining_profiles:
            # Обновляем список ID в состоянии
            data.ids = remaining_profiles
            await data.save(state)
            
            # Показываем первый профиль
            first_id = remaining_profiles[0]
            
            # Обновляем username пользователя из Telegram перед показом профиля
            await update_user_username_from_telegram(session, first_id)
            
            profile = await Profile.get(session, first_id)
            await display_filtered_profile(session, user.id, profile, user.language, user.id)
            return
        else:
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
        # Пытаемся дать шанс (функция сама сохранит состояние при недостатке шансов)
        await _give_chance(
            message=message,
            user=user,
            another_user=another_user,
            session=session,
            state=state,
            search_data=data,
        )
        return

    # Ветка "Меню поиска"
    if message.text in KB_BACK_TO_SEARCH_V:
        # Очищаем состояние поиска и возвращаемся к меню поиска
        await state.clear()
        await send_filter(session, message.from_user.id, user)
        return

    # Иначе: «Далее» — показать следующего
    
    await _show_next_profile(session, message, state, user, data)


async def _give_chance(message: types.Message, user: UserModel, another_user: UserModel, session: AsyncSession, state: FSMContext = None, search_data: SearchData = None) -> None:
    # Проверяем, достаточно ли шансов для дачи шанса
    if user.balance_chances < 1:
        if state and search_data:
            # Сохраняем состояние поиска для продолжения после оплаты
            search_data.paused_for_payment = True
            await search_data.save(state)
            logger.log("GIVE_CHANCE_DEBUG", f"user={user.id} saved_search_state_for_payment, mode={search_data.mode}")
        
        await message.answer(
            f"❌ Недостаточно шансов для дачи шанса. У вас {user.balance_chances} шанс(ов).",
            reply_markup=payment_kb()
        )
        return

    # Списываем 1 шанс перед созданием матча
    try:
        await User.use_one_chance(session=session, user=user, target_id=another_user.id)
        await session.refresh(user)  # Обновляем баланс пользователя
        logger.log("BALANCE_DEBUG", f"user={user.id} -1 (give_chance via use_one_chance)")
    except ValueError as e:
        logger.log("BALANCE_DEBUG", f"user={user.id} ValueError caught in give_chance: {e}")
        raise ValueError("Недостаточно шансов для дачи шанса")
    except Exception as e:
        logger.log("BALANCE_DEBUG", f"user={user.id} use_one_chance failed: {e!r}")
        await message.answer(mt.ERR_CHANCES_DEBIT_FAILED, parse_mode=ParseMode.HTML)
        return

    # Создаем матч
    is_create = await Match.create(session, message.from_user.id, another_user.id, None)
    if not is_create:
        return

    # Получаем обновленный баланс и обновляем объект пользователя
    await session.refresh(user)
    user_balance = await User.get_chance_balance(user)
    
    # Обновляем username пользователя из Telegram перед формированием ссылки
    updated_username = await update_user_username_from_telegram(session, another_user.id)
    
    profile_link = (
        f"https://t.me/{updated_username}"
        if updated_username
        else f"tg://user?id={another_user.id}"
    )

    await message.answer(text=mt.GAVE_CHANCE(profile_link, user_balance), parse_mode=ParseMode.HTML, reply_markup=search_kb_after_chance(), disable_web_page_preview=True)

    # Уведомим получателя шанса: отправим ему профиль дарителя и ссылку на контакт
    await send_got_chance_alert(session=session, recipient=another_user, giver=user)

async def _show_next_profile(
    session: AsyncSession,
    message: types.Message,
    state: FSMContext,
    user: UserModel,
    data: SearchData,
) -> None:
    ids = data.ids
    if not ids:
        # Проверяем, есть ли профили по текущему фильтру
        remaining_profiles = await search_profiles(session, user.profile)
        if remaining_profiles:
            # Обновляем список ID в состоянии
            data.ids = remaining_profiles
            await data.save(state)
            
            # Показываем первый профиль
            first_id = remaining_profiles[0]
            profile = await Profile.get(session, first_id)
            await display_filtered_profile(session, user.id, profile, user.language, user.id)
            return
        else:
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
            # Получаем заново список профилей по текущему фильтру
            profile_list = await search_profiles(session, user.profile)
            if profile_list:
                # Обновляем список ID в состоянии
                data.ids = profile_list
                await data.save(state)
                
                # Показываем первый профиль
                first_id = profile_list[0]
                
                # Обновляем username пользователя из Telegram перед показом профиля
                await update_user_username_from_telegram(session, first_id)
                
                profile = await Profile.get(session, first_id)
                await display_filtered_profile(session, user.id, profile, user.language, user.id)
                return
            else:
                # Если профили не найдены, показываем сообщение об ошибке
                await message.answer(mt.INVALID_PROFILE_SEARCH)

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

    # Обновляем username пользователя из Telegram перед показом профиля
    await update_user_username_from_telegram(session, next_id)

    profile = await Profile.get(session, next_id)
    await display_filtered_profile(session, user.id, profile, user.language, user.id)


# ---------- Функция для проверки и возобновления приостановленного поиска ----------

async def check_and_resume_paused_search(
    message: types.Message, 
    state: FSMContext, 
    user: UserModel, 
    session: AsyncSession
) -> bool:
    """
    Проверяет, есть ли приостановленный поиск, и если да - предлагает продолжить.
    Возвращает True, если поиск был возобновлен, False - если нет.
    """
    current_state = await state.get_state()
    logger.log("RESUME_SEARCH_DEBUG", f"user={user.id} checking_paused_search, current_state={current_state}")
    
    if current_state != Search.search:
        logger.log("RESUME_SEARCH_DEBUG", f"user={user.id} not_in_search_state")
        return False
    
    data = await SearchData.load(state)
    logger.log("RESUME_SEARCH_DEBUG", f"user={user.id} loaded_search_data, paused={data.paused_for_payment}, ids_count={len(data.ids)}")
    
    if not data.paused_for_payment or not data.ids:
        logger.log("RESUME_SEARCH_DEBUG", f"user={user.id} no_paused_search_or_empty_ids")
        return False
    
    # Проверяем баланс после оплаты
    await session.refresh(user)  # Обновляем баланс пользователя
    balance_now = user.balance_chances
    
    # ЛОГИКА: 
    # - Для умного поиска: 3 шанса уже списаны при запуске, нужно только 1 для "дать шанс"
    # - Для обычного поиска: шансы не списывались, нужно только 1 для "дать шанс"
    # - В любом случае для продолжения просмотра достаточно 1 шанса
    required_chances = 1
    
    logger.log("RESUME_SEARCH_DEBUG", f"user={user.id} mode={data.mode} balance={balance_now} required={required_chances}")
    
    if balance_now < required_chances:
        # Баланс все еще недостаточен
        logger.log("RESUME_SEARCH_DEBUG", f"user={user.id} insufficient_balance_for_resume: {balance_now} < {required_chances}")
        await message.answer(
            f"❌ Недостаточно шансов для продолжения поиска. У вас {balance_now} шанс(ов), требуется {required_chances}.",
            reply_markup=payment_kb()
        )
        return False
    
    # Баланс достаточен, возобновляем поиск
    data.paused_for_payment = False
    await data.save(state)
    
    # Показываем текущий профиль (тот, для которого пользователь хотел дать шанс)
    current_id = data.ids[0]
    another_user = await User.get_with_profile(session, current_id)
    
    if not another_user:
        await message.answer(mt.INVALID_PROFILE_SEARCH, reply_markup=search_menu_kb(user=user))
        await state.clear()
        return True
    
    # Показываем ТОТ ЖЕ профиль, для которого пользователь хотел дать шанс
    if data.mode == "ai":
        reason_text = data.ai_reasons.get(str(current_id))
        if reason_text:
            await message.answer(text=mt.SMART_SEARCH_MATCH_REASON(reason=reason_text))
    
    # Обновляем username пользователя из Telegram перед показом профиля
    await update_user_username_from_telegram(session, current_id)
    
    await display_filtered_profile(session, user.id, another_user.profile, user.language, user.id)
    
    await message.answer(
        "✅ Теперь у вас достаточно шансов! Вы можете дать шанс этому пользователю или продолжить поиск.",
        reply_markup=search_kb()
    )
    
    logger.log("RESUME_SEARCH_DEBUG", f"user={user.id} resumed_search_with_same_profile={current_id}")
    
    return True
