import requests
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart

import keyboards as kb

router = Router()

class Currency:
    def __init__(self):
        self.basic = None
        self.target = None

currency = Currency()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        'Select the currency you want to convert to another currency!',
        reply_markup=kb.main_buttons
    )

@router.callback_query(F.data.in_({'USD', 'RUB'}))
async def base_currency(callback: CallbackQuery):
    currency.basic = callback.data
    await callback.answer()
    await callback.message.edit_text(
        f'You chose the {callback.data}.',
        reply_markup=kb.main_buttons_2
    )

@router.callback_query(F.data.in_({'USD_2', 'RUB_2'}))
async def target_currency(callback: CallbackQuery):
    currency.target = callback.data
    await callback.answer()
    await callback.message.edit_text(
        f'You chose to convert to {callback.data}. Now, please enter the amount to convert:'
    )

@router.message(F.text.isdigit())  # Фильтр отслеживает сообщения, содержащие только цифры
async def conversion(message: Message):
    # Проверка, выбрал ли пользователь базовую и целевую валюту
    if not currency.basic or not currency.target:
        await message.answer("Please select the currencies before entering the amount!")
        return

    try:
        # Преобразуем текст сообщения в число
        amount = float(message.text)

        # Проверка, чтобы currency.basic был корректным
        if currency.basic is None:
            await message.answer("Base currency is not set!")
            return

        # Формируем запрос к API
        url = f"https://api.exchangerate-api.com/v4/latest/{currency.basic}"
        response = requests.get(url)

        # Проверка успешности запроса
        if response.status_code == 200:
            data = response.json()

            # Извлечение целевой валюты без "_2"
            target_currency = currency.target.split('_')[0]

            # Проверка наличия целевой валюты в данных API
            if target_currency in data["rates"]:
                conversion_rate = data["rates"][target_currency]
                converted_amount = amount * conversion_rate
                await message.answer(f"Converted amount: {converted_amount}")
            else:
                await message.answer("Target currency not found in exchange rates!")
        else:
            await message.answer("Failed to retrieve exchange rate data!")
    except ValueError:
        await message.answer("Invalid amount format. Please enter a valid number!")
    except Exception as e:
        await message.answer(f"An unexpected error occurred: {e}")

