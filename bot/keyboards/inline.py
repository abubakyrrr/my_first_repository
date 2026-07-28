from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_main_keyboard(is_premium: bool = False) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="Выбрать валюты", callback_data="select_currency"),
            InlineKeyboardButton(text="Выбрать города", callback_data="select_city")
        ],
        [InlineKeyboardButton(text="Моя сводка (Погода + Курсы)", callback_data="get_summary")]
    ]

    if not is_premium:
        buttons.append([
            InlineKeyboardButton(text="Купить Premium (100 Звезд)", callback_data="buy_premium")
        ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_currency_keyboard(selected_currencies: list) -> InlineKeyboardMarkup:
    currencies = ["USD", "EUR", "RUB", "KZT", "CNY", "TRY"]
    buttons = []

    for curr in currencies:
        mark = "✔️ " if curr in selected_currencies else ""
        buttons.append([InlineKeyboardButton(
            text=f"{mark}{curr}",
            callback_data=f"toggle_curr_{curr}"
        )])

    buttons.append([InlineKeyboardButton(text="Назад", callback_data="main_menu")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)