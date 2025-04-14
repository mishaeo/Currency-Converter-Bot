import requests
from enum import Enum
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart

import keyboards as kb

router = Router()

# Список валют
class CurrencyEnum(str, Enum):
    USD = "USD"
    RUB = "RUB"

# Состояния бота
class CurrencyConversion(StatesGroup):
    choosing_base = State()
    choosing_target = State()
    entering_amount = State()

# /start — запуск
@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "👋 Привет! Выберите валюту, из которой хотите конвертировать:",
        reply_markup=kb.main_buttons
    )
    await state.set_state(CurrencyConversion.choosing_base)

# Выбор базовой валюты
@router.callback_query(F.data.in_({c.value for c in CurrencyEnum}))
async def choose_base(callback: CallbackQuery, state: FSMContext):
    await state.update_data(base=callback.data)
    await callback.answer()
    await callback.message.edit_text(
        f"Вы выбрали базовую валюту: {callback.data}\nТеперь выберите целевую валюту:",
        reply_markup=kb.main_buttons_2
    )
    await state.set_state(CurrencyConversion.choosing_target)

# Выбор целевой валюты
@router.callback_query(F.data.in_({f"{c.value}_2" for c in CurrencyEnum}))
async def choose_target(callback: CallbackQuery, state: FSMContext):
    target_currency = callback.data.replace("_2", "")
    await state.update_data(target=target_currency)
    await callback.answer()
    await callback.message.edit_text(
        f"Целевая валюта: {target_currency}. Введите сумму для конвертации:"
    )
    await state.set_state(CurrencyConversion.entering_amount)

# Ввод суммы и расчет
@router.message(CurrencyConversion.entering_amount, F.text)
async def convert_amount(message: Message, state: FSMContext):
    data = await state.get_data()
    base = data.get("base")
    target = data.get("target")

    try:
        amount = float(message.text)
        if amount <= 0:
            raise ValueError

        url = f"https://api.exchangerate-api.com/v4/latest/{base}"
        response = requests.get(url)
        response.raise_for_status()

        rates = response.json().get("rates", {})
        rate = rates.get(target)

        if rate:
            result = round(amount * rate, 2)
            await message.answer(f"{amount} {base} = {result} {target}")
        else:
            await message.answer("Ошибка: Целевая валюта не найдена в курсах.")

    except ValueError:
        await message.answer("Пожалуйста, введите корректную положительную сумму.")
    except Exception as e:
        await message.answer(f"Произошла ошибка при получении данных: {e}")

    await state.clear()
