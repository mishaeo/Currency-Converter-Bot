from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from currency import Currency  # Импорт Enum из твоего основного файла

def build_currency_keyboard(suffix: str = "") -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(
            text=currency.display_name,
            callback_data=f"{currency.value}{suffix}"
        )
        for currency in Currency
    ]

    # делим по 2-3 кнопки в ряд
    row_width = 2
    keyboard = [buttons[i:i + row_width] for i in range(0, len(buttons), row_width)]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)

# Основные клавиатуры
main_button = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Convert currency")]
    ],
    resize_keyboard=True
)

# Отдельные клавиатуры для базовой и целевой валют
base_button = build_currency_keyboard()
target_button = build_currency_keyboard("_2")

