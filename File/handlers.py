import logging
import httpx

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart

from currency import Currency
import keyboards as kb

router = Router()
logger = logging.getLogger(__name__)

# States for the FSM
class ConversionState(StatesGroup):
    base_currency = State()
    target_currency = State()
    amount_input = State()

# /start handler
@router.message(CommandStart())
async def handle_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "👋 Welcome to the currency converter bot!",
        reply_markup=kb.main_button
    )

# Start conversion process
@router.message(F.text == 'Convert currency')
async def start_conversion(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Please choose the base currency:",
        reply_markup=kb.base_button
    )
    await state.set_state(ConversionState.base_currency)

# Handle base currency selection
@router.callback_query(F.data.in_({c.value for c in Currency}))
async def handle_base_currency(callback: CallbackQuery, state: FSMContext):
    base = callback.data
    await state.update_data(base=base)
    await callback.answer()

    await callback.message.edit_text(
        f"✅ Base currency selected: {Currency(base).display_name}\n"
        f"Now choose the target currency:",
        reply_markup=kb.target_button
    )
    await state.set_state(ConversionState.target_currency)

# Handle target currency selection
@router.callback_query(F.data.in_({f"{c.value}_2" for c in Currency}))
async def handle_target_currency(callback: CallbackQuery, state: FSMContext):
    target = callback.data.replace("_2", "")
    data = await state.get_data()
    base = data.get("base")

    if base == target:
        await callback.answer()
        await callback.message.edit_text("⚠️ Base and target currencies must be different. Please choose again.")
        return

    await state.update_data(target=target)
    await callback.answer()

    await callback.message.edit_text(
        f"🎯 Target currency selected: {Currency(target).display_name}\n"
        f"Please enter the amount to convert:"
    )
    await state.set_state(ConversionState.amount_input)

# Fetch exchange rate from API
async def get_exchange_rate(base: str, target: str) -> float | None:
    url = f"https://api.exchangerate-api.com/v4/latest/{base}"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10)
            response.raise_for_status()
            rates = response.json().get("rates", {})
            return rates.get(target)
    except Exception as e:
        logger.error(f"Failed to fetch exchange rate: {e}")
        return None

# Handle amount input and calculate result
@router.message(ConversionState.amount_input, F.text)
async def handle_amount_input(message: Message, state: FSMContext):
    data = await state.get_data()
    base = data.get("base")
    target = data.get("target")

    try:
        amount = float(message.text)
        if amount <= 0:
            raise ValueError

        rate = await get_exchange_rate(base, target)
        if rate is None:
            await message.answer("⚠️ Failed to fetch exchange rate. Please try again later.")
        else:
            result = round(amount * rate, 2)
            await message.answer(f"💱 {amount} {base} = {result} {target}")

    except ValueError:
        await message.answer("❌ Please enter a valid positive number.")
    except Exception as e:
        logger.exception("Unexpected error during conversion")
        await message.answer("🚨 An unexpected error occurred. Please try again.")

    await state.clear()
