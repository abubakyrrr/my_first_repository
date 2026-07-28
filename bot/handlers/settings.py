from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from bot.database.db import get_user, update_user_selection
from bot.keyboards.inline import get_items_keyboard, get_main_keyboard
from bot.config import FREE_CURRENCY_LIMIT, FREE_WEATHER_LIMIT
from bot.services.weather import get_weather
from bot.services.currency import is_valid_currency

router = Router()

@router.callback_query(F.data == "select_currency")
async def process_select_currency(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_data = get_user(user_id)
    currencies = user_data["currencies"] if user_data else []

    text = "Твои отслеживаемые валюты:\n"
    if currencies:
        for c in currencies:
            text += f"- {c}\n"
    else:
        text += "Список пуст.\n"

    text += "\nНапиши трехзначный код любой валюты (например: USD, EUR, JPY, KZT) в чат!"

    await callback.message.edit_text(text, reply_markup=get_items_keyboard(currencies, "curr"))
    await callback.answer()

@router.callback_query(F.data.startswith("remove_curr_"))
async def process_remove_currency(callback: CallbackQuery):
    user_id = callback.from_user.id
    curr = callback.data.split("_")[2]

    user_data = get_user(user_id)
    currencies = user_data["currencies"]
    cities = user_data["cities"]

    if curr in currencies:
        currencies.remove(curr)

    update_user_selection(user_id, currencies, cities)

    text = "Твои отслеживаемые валюты:\n"
    if currencies:
        for c in currencies:
            text += f"- {c}\n"
    else:
        text += "Список пуст.\n"

    text += "\nНапиши трехзначный код любой валюты (например: USD, EUR, JPY, KZT) в чат!"

    await callback.message.edit_text(text, reply_markup=get_items_keyboard(currencies, "curr"))
    await callback.answer()

@router.callback_query(F.data == "select_city")
async def process_select_city(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_data = get_user(user_id)
    cities = user_data["cities"] if user_data else []

    text = "Твои сохраненные города:\n"
    if cities:
        for c in cities:
            text += f"- {c}\n"
    else:
        text += "Список пуст.\n"

    text += "\nНапиши название любого города в чат, чтобы добавить его!"

    await callback.message.edit_text(text, reply_markup=get_items_keyboard(cities, "city"))
    await callback.answer()

@router.callback_query(F.data.startswith("remove_city_"))
async def process_remove_city(callback: CallbackQuery):
    user_id = callback.from_user.id
    city = callback.data.split("_")[2]

    user_data = get_user(user_id)
    currencies = user_data["currencies"]
    cities = user_data["cities"]

    if city in cities:
        cities.remove(city)

    update_user_selection(user_id, currencies, cities)

    text = "Твои сохраненные города:\n"
    if cities:
        for c in cities:
            text += f"- {c}\n"
    else:
        text += "Список пуст.\n"

    text += "\nНапиши название любого города в чат, чтобы добавить его!"

    await callback.message.edit_text(text, reply_markup=get_items_keyboard(cities, "city"))
    await callback.answer()

@router.callback_query(F.data == "get_summary")
async def process_get_summary(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_data = get_user(user_id)

    currencies = ", ".join(user_data["currencies"]) if user_data and user_data["currencies"] else "Не выбраны"
    cities = ", ".join(user_data["cities"]) if user_data and user_data["cities"] else "Не выбраны"

    await callback.message.answer(
        f"Твоя сводка:\n\n"
        f"Валюты: {currencies}\n"
        f"Города: {cities}"
    )
    await callback.answer()

@router.callback_query(F.data == "main_menu")
async def process_main_menu(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_data = get_user(user_id)
    is_premium = user_data["is_premium"] if user_data else False

    status_text = "Премиум-аккаунт" if is_premium else "Бесплатный тариф"
    text = (
        f"Главное меню\n\n"
        f"Твой статус: {status_text}\n"
        f"Выбирай валюты и города:"
    )

    await callback.message.edit_text(text, reply_markup=get_main_keyboard(is_premium))
    await callback.answer()

@router.message(F.text & ~F.text.startswith("/"))
async def process_add_item_by_text(message: Message):
    user_id = message.from_user.id
    user_input = message.text.strip()

    user_data = get_user(user_id)
    if not user_data:
        return

    currencies = user_data["currencies"]
    cities = user_data["cities"]
    is_premium = user_data["is_premium"]

    if len(user_input) == 3 and user_input.isalpha():
        curr_code = user_input.upper()

        if curr_code in currencies:
            await message.answer(f"Валюта {curr_code} уже есть в списке!")
            return

        if not is_premium and len(currencies) >= FREE_CURRENCY_LIMIT:
            await message.answer(f"Лимит {FREE_CURRENCY_LIMIT} валюты! Купи Премиум для снятия ограничений.")
            return

        if not await is_valid_currency(curr_code):
            await message.answer("Валюта не найдена. Проверь код (например: USD, EUR, RUB, KZT).")
            return

        currencies.append(curr_code)
        update_user_selection(user_id, currencies, cities)
        await message.answer(f"Валюта {curr_code} успешно добавлена!")
        return

    city_name = user_input.title()

    if city_name in cities:
        await message.answer(f"Город {city_name} уже есть в списке!")
        return

    if not is_premium and len(cities) >= FREE_WEATHER_LIMIT:
        await message.answer(f"Лимит {FREE_WEATHER_LIMIT} города! Купи Премиум для снятия ограничений.")
        return

    weather_info = await get_weather(city_name)
    if weather_info == "Не удалось получить данные":
        await message.answer("Город или валюта не найдены. Проверь правильность ввода.")
        return

    cities.append(city_name)
    update_user_selection(user_id, currencies, cities)
    await message.answer(f"Город {city_name} добавлен!\nПогода сейчас: {weather_info}")