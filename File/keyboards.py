from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

main_buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='$ - USD (United States Dollar)', callback_data='USD'),
         InlineKeyboardButton(text='₽ - RUB (Russian Ruble)', callback_data='RUB')]
    ]
)

main_buttons_2 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='$ - USD (United States Dollar)', callback_data='USD_2'),
         InlineKeyboardButton(text='₽ - RUB (Russian Ruble)', callback_data='RUB_2')]
    ]
)
