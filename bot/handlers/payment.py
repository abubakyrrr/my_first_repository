from aiogram import Router, F
from aiogram.types import CallbackQuery, LabeledPrice, PreCheckoutQuery, Message
from bot.config import PREMIUM_PRICE
from bot.database.db import set_premium

router = Router()

@router.callback_query(F.data == "buy_premium")
async def process_buy_premium(callback: CallbackQuery):
    prices = [LabeledPrice(label="Premium статус", amount=PREMIUM_PRICE)]

    await callback.message.answer_invoice(
        title="Премиум Доступ",
        description="Снимает все ограничения на количество отслеживаемых валют и городов!",
        payload="premium_buy_stars",
        currency="XTR",
        prices=prices,
        start_parameter="buy-premium"
    )
    await callback.answer()

@router.pre_checkout_query()
async def process_pre_checkout(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)

@router.message(F.successful_payment)
async def process_successful_payment(message: Message):
    user_id = message.from_user.id
    set_premium(user_id)

    await message.answer("Поздравляем! Премиум-статус успешно активирован. Все лимиты сняты!")