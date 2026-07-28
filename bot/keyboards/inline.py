from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_main_keyboard(is_premium: bool = False) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="Выбрать валюты", callback_data="select_currency"),
            InlineKeyboardButton(text="Выбрать города", callback_data="select_city")
        ],
        [InlineKeyboardButton(text="Моя сводка", callback_data="get_summary")]
    ]

    if not is_premium:
        buttons.append([
            InlineKeyboardButton(text="Купить Premium (100 Звезд)", callback_data="buy_premium")
        ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_items_keyboard(items: list, item_type: str) -> InlineKeyboardMarkup:
    buttons = []

    for item in items:
        buttons.append([InlineKeyboardButton(
            text=f"Удалить {item}",
            callback_data=f"remove_{item_type}_{item}"
        )])

    buttons.append([InlineKeyboardButton(text="Назад", callback_data="main_menu")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)