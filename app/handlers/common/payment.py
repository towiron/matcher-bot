from aiogram import types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, LabeledPrice

from data.config import CLICK_LIVE_TOKEN
from database.models import UserModel
from database.models.balance_top_up import TopUpSource
from database.services import User
from loader import _

from app.routers import common_router

from app.text import message_text as mt

@common_router.message(F.text == "/pay")
async def choose_chance(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🧿 Купить 1 шанс — 1000 сум", callback_data="buy_chances:1")],
        [InlineKeyboardButton(text="🧿 Купить 3 шанса — 3000 сум", callback_data="buy_chances:3")],
        [InlineKeyboardButton(text="🧿 Купить 10 шансов — 10000 сум", callback_data="buy_chances:10")],
    ])
    await message.answer("Выберите количество шансов для покупки:", reply_markup=keyboard)

@common_router.callback_query(F.data.startswith("buy_chances:"))
async def handle_buy_chances(callback: types.CallbackQuery):
    chance_count = int(callback.data.split(":")[1])
    price = chance_count * 1000  # 1000 сум за шанс
    title = f"Покупка {chance_count} шанс(ов)"

    prices = [LabeledPrice(label=title, amount=price * 100)]  # умножаем на 100 (копейки)

    await callback.message.answer_invoice(
        title=title,
        description=f"Покупка {chance_count} шанс(ов) для использования в боте.",
        provider_token=CLICK_LIVE_TOKEN,
        currency="UZS",
        prices=prices,
        payload=f"buy:{chance_count}",  # можно использовать в webhook или success_payment
    )
    await callback.answer()

@common_router.pre_checkout_query()
async def pre_checkout_handler(query: types.PreCheckoutQuery):
    await query.answer(ok=True)


@common_router.message(F.successful_payment)
async def on_successful_payment(message: types.Message, user: UserModel, session):
    payload = message.successful_payment.invoice_payload  # 'buy:3'
    chance_count = int(payload.split(":")[1])
    paid_sum = message.successful_payment.total_amount // 100  # копейки → сума

    await User.add_chances_from_payment(
        session=session,
        user=user,
        paid_sum=paid_sum,
        payload=payload,
        source=TopUpSource.Click,
    )

    await message.answer(f"✅ Оплата прошла успешно! Вы купили {chance_count} шанс(ов).")
    total_balance = await User.get_chance_balance(user)
    await message.answer(f"На вашем балансе {total_balance} шанс(ов).")

