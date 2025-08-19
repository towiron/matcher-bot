from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, LabeledPrice, ReplyKeyboardRemove

from app.business.menu_service import menu
from app.keyboards.default.base import menu_kb
from data.config import CLICK_LIVE_TOKEN, PAYME_LIVE_TOKEN, CHANCE_COST
from database.models import UserModel
from app.routers import common_router
from app.text import message_text as mt

# ⚙️ Новый леджер/энумы
from database.services.balance import Balance
from database.models.enums import EntryKind, Source

PLANS = [
    {"sum": 5_000,  "chances": 5},
    {"sum": 10_000, "chances": 11},  # +1 бонус
    {"sum": 20_000, "chances": 22},  # +2 бонус
    {"sum": 40_000, "chances": 44},  # +4 бонус
    {"sum": 50_000, "chances": 55},  # +5 бонус
]
PLANS_BY_SUM = {p["sum"]: p for p in PLANS}

# Провайдеры и токены оплаты
PAYMENT_PROVIDER_TOKENS = {
    "click": CLICK_LIVE_TOKEN,
    "payme": PAYME_LIVE_TOKEN,
    # "uzum": UZUM_LIVE_TOKEN,
}

# Маппинг на Source enum
SOURCES = {
    "click": Source.Click,
    "payme": Source.Payme,
    "uzum": Source.Uzum,
}


def fmt_sum(v: int) -> str:
    # 10 000 -> '10 000' (неразрывный пробел)
    return f"{v:,}".replace(",", " ").replace(" ", "\u00A0")


@common_router.message(F.text.in_(("/pay", mt.KB_BUY_CHANCES)))
async def choose_provider(message: types.Message, user: UserModel):
    # показываем баланс в шансах из кеша
    balance_chances = getattr(user, "balance_chances", None)
    if balance_chances is None:
        # на всякий случай бэкап, если старый метод ещё живёт
        from database.services import User as OldUserSvc
        balance_chances = await OldUserSvc.get_chance_balance(user)

    await message.answer(
        text=f"💎 На вашем балансе {balance_chances} шанс(ов)",
        reply_markup=ReplyKeyboardRemove()
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Click", callback_data="provider:click")],
        [InlineKeyboardButton(text="💳 Payme", callback_data="provider:payme")],
        # [InlineKeyboardButton(text="💳 Uzum", callback_data="provider:uzum")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="buy:back")]
    ])
    await message.answer("Выберите платёжную систему:", reply_markup=keyboard)


@common_router.callback_query(F.data == "buy:back")
async def back_to_menu(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
    await menu(callback.from_user.id)


@common_router.callback_query(F.data.startswith("provider:"))
async def choose_sum(callback: types.CallbackQuery):
    provider = callback.data.split(":")[1]
    rows = []
    for p in PLANS:
        s = fmt_sum(p["sum"])
        c = p["chances"]
        rows.append([
            InlineKeyboardButton(
                text=f"💎 {s} сум — {c} шанс(ов)",
                callback_data=f"buy_sum:{provider}:{p['sum']}"
            )
        ])
    rows.append([InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_providers")])

    keyboard = InlineKeyboardMarkup(inline_keyboard=rows)
    await callback.message.edit_text("Выберите сумму пополнения:", reply_markup=keyboard)


@common_router.callback_query(F.data == "back_to_providers")
async def back_to_providers(callback: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Click", callback_data="provider:click")],
        [InlineKeyboardButton(text="💳 Payme", callback_data="provider:payme")],
        # [InlineKeyboardButton(text="💳 Uzum", callback_data="provider:uzum")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="buy:back")]
    ])
    await callback.message.edit_text("Выберите платёжную систему:", reply_markup=keyboard)


@common_router.callback_query(F.data.startswith("buy_sum:"))
async def handle_buy_sum(callback: types.CallbackQuery):
    _, provider, sum_str = callback.data.split(":")
    paid_sum = int(sum_str)
    plan = PLANS_BY_SUM.get(paid_sum)

    token = PAYMENT_PROVIDER_TOKENS.get(provider)
    if not token or not plan:
        await callback.answer("Неверные параметры оплаты.", show_alert=True)
        return

    chance_count = plan["chances"]
    title = f"Покупка шансов — {chance_count} шт."
    description = (
        f"💎 Вы покупаете {chance_count} шанс(ов).\n"
        f"💰 К оплате: {fmt_sum(paid_sum)} сум.\n"
        "Нажмите кнопку ниже, чтобы перейти к оплате."
    )

    prices = [LabeledPrice(label=f"{chance_count} шанс(ов)", amount=paid_sum * 100)]  # UZS → 'коины'

    await callback.message.answer_invoice(
        title=title,
        description=description,
        provider_token=token,
        currency="UZS",
        prices=prices,
        payload=f"buy:{provider}:{paid_sum}",   # ⬅️ передаём сумму
    )
    await callback.answer()


@common_router.pre_checkout_query()
async def pre_checkout_handler(query: types.PreCheckoutQuery):
    await query.answer(ok=True)


@common_router.message(F.successful_payment)
async def on_successful_payment(message: types.Message, user: UserModel, session, state: FSMContext):
    # Распарсим payload
    try:
        _, provider, sum_str = message.successful_payment.invoice_payload.split(":")
        requested_sum = int(sum_str)
    except Exception:
        await message.answer("Ошибка в данных оплаты.")
        return

    paid_sum = message.successful_payment.total_amount // 100  # факт от Telegram
    if paid_sum != requested_sum:
        await message.answer("Сумма оплаты не совпадает с запросом.", reply_markup=menu_kb)
        return

    plan = PLANS_BY_SUM.get(paid_sum)
    if not plan:
        await message.answer("Неизвестный тариф.", reply_markup=menu_kb)
        return

    source = SOURCES.get(provider)
    if not source:
        await message.answer("Неизвестный провайдер оплаты.", reply_markup=menu_kb)
        return

    # Считаем оплаченные и бонусные шансы
    paid_chances = Balance.sum_to_chances(paid_sum)
    bonus_chances = plan["chances"] - paid_chances

    # 1) оплаченная часть (TOP_UP / provider)
    await Balance.credit(
        session=session,
        user=user,
        delta_chances=paid_chances,
        kind=EntryKind.TOP_UP,
        source=source,
        amount_sum=paid_sum,
        payload=message.successful_payment.invoice_payload,
    )

    # 2) бонус (BONUS / Internal)
    if bonus_chances > 0:
        await Balance.credit(
            session=session,
            user=user,
            delta_chances=bonus_chances,
            kind=EntryKind.BONUS,
            source=Source.Internal,
            amount_sum=bonus_chances * CHANCE_COST,  # опционально для отчётов
            payload=f"bonus:bundle_{paid_sum}",
        )

    await message.answer(f"✅ Оплата прошла успешно! 💎 Зачислено {plan['chances']} шанс(ов).")
    total = getattr(user, "balance_chances", None)
    if total is None:
        from database.services import User as OldUserSvc
        total = await OldUserSvc.get_chance_balance(user)

    await state.clear()
    await message.answer(f"💎 На вашем балансе {total} шанс(ов).", reply_markup=menu_kb)
