from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from bot.database.db import add_user, get_user
from bot.keyboards.inline import get_main_keyboard

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    user_id = message.from_user.id
    add_user(user_id)

    user_data = get_user(user_id)
    is_premium = user_data["is_premium"] if user_data else False

    status_text = "**Премиум-аккаунт** (Без лимитов)" if is_premium else "**Бесплатный тариф** (До 3 валют и 2 городов)"

    text = (
        f"Привет, {message.from_user.first_name}!\n\n"
        f"Твой статус: {status_text}\n"
        f"Выбирай валюты и города для получения ежедневной сводки:"
    )

    await message.answer(text, reply_markup=get_main_keyboard(is_premium), parse_mode="Markdown")