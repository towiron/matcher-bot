from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, LabeledPrice, ReplyKeyboardRemove

from app.business.menu_service import menu
from app.keyboards.default.base import menu_kb
from data.config import CLICK_LIVE_TOKEN, CHANCE_COST
from database.models import UserModel
from database.models.balance_top_up import TopUpSource
from database.services import User
from loader import _
from app.routers import common_router
from app.text import message_text as mt

# Провайдеры и токены оплаты
PAYMENT_PROVIDER_TOKENS = {
    "click": CLICK_LIVE_TOKEN,
    # "payme": PAYME_LIVE_TOKEN,
    # "uzum": UZUM_LIVE_TOKEN,
}

TOP_UP_SOURCES = {
    "click": TopUpSource.Click,
    "payme": TopUpSource.Payme,
    "uzum": TopUpSource.Uzum,
}


@common_router.message(F.text.in_(("/pay", _(mt.KB_BUY_CHANCES))))
async def choose_provider(message: types.Message, user: UserModel):
    balance =  await User.get_chance_balance(user)
    await message.answer(text=f"💎На вашем балансе {balance} шанс(ов)", reply_markup=ReplyKeyboardRemove())
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Click", callback_data="provider:click")],
        # [InlineKeyboardButton(text="💳 Payme", callback_data="provider:payme")],
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
async def choose_chance(callback: types.CallbackQuery):
    provider = callback.data.split(":")[1]
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💎 Купить 1 шанс — 1000 сум", callback_data=f"buy_chances:{provider}:1")],
        [InlineKeyboardButton(text="💎 Купить 3 шанса — 3000 сум", callback_data=f"buy_chances:{provider}:3")],
        [InlineKeyboardButton(text="💎 Купить 10 шансов — 10000 сум", callback_data=f"buy_chances:{provider}:10")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_providers")],
    ])
    await callback.message.edit_text("Выберите количество шансов для покупки:", reply_markup=keyboard)


@common_router.callback_query(F.data == "back_to_providers")
async def back_to_providers(callback: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Click", callback_data="provider:click")],
        # [InlineKeyboardButton(text="💳 Payme", callback_data="provider:payme")],
        # [InlineKeyboardButton(text="💳 Uzum", callback_data="provider:uzum")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="buy:back")]
    ])
    await callback.message.edit_text("Выберите платёжную систему:", reply_markup=keyboard)


@common_router.callback_query(F.data.startswith("buy_chances:"))
async def handle_buy_chances(callback: types.CallbackQuery):
    _, provider, count_str = callback.data.split(":")
    chance_count = int(count_str)
    price = chance_count * CHANCE_COST

    token = PAYMENT_PROVIDER_TOKENS.get(provider)
    if not token:
        await callback.answer("Выбранный провайдер не поддерживается.", show_alert=True)
        return

    title = f"Покупка шансов — {chance_count} шт."
    description = (
        f"💎 Вы собираетесь купить {chance_count} шанс(ов).\n"
        f"💰 Стоимость: {price} сум.\n"
        "Нажмите кнопку ниже, чтобы перейти к оплате."
    )

    prices = [LabeledPrice(label=f"{chance_count} шанс(ов)", amount=price * 100)]

    await callback.message.answer_invoice(
        title=title,
        description=description,
        provider_token=token,
        currency="UZS",
        prices=prices,
        payload=f"buy:{provider}:{chance_count}",
    )
    await callback.answer()


@common_router.pre_checkout_query()
async def pre_checkout_handler(query: types.PreCheckoutQuery):
    await query.answer(ok=True)


@common_router.message(F.successful_payment)
async def on_successful_payment(message: types.Message, user: UserModel, session, state: FSMContext):
    try:
        _, provider, count_str = message.successful_payment.invoice_payload.split(":")
        chance_count = int(count_str)
    except Exception:
        await message.answer("Ошибка в данных оплаты.")
        return

    paid_sum = message.successful_payment.total_amount // 100
    source = TOP_UP_SOURCES.get(provider)

    if not source:
        await message.answer("Неизвестный провайдер оплаты.")
        return

    await User.add_chances_from_payment(
        session=session,
        user=user,
        paid_sum=paid_sum,
        payload=message.successful_payment.invoice_payload,
        source=source,
    )

    await message.answer(f"✅ Оплата прошла успешно! 💎 Вы купили {chance_count} шанс(ов).")
    total_balance = await User.get_chance_balance(user)
    await state.clear()
    await message.answer(f"💎 На вашем балансе {total_balance} шанс(ов).", reply_markup=menu_kb)
