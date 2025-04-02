from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart

import keyboards as kb

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Select the currency you want to convert to another currency!', reply_markup=kb.main_buttons)

@router.callback_query(F.data.in_({'USD', 'RUB'}))
async def catalog(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(f'You chose the {callback.data}.', reply_markup=kb.main_buttons_2)

@router.callback_query(F.data.in_({'USD_2', 'RUB_2'}))
async def catalog_2(callback: CallbackQuery):
    target_currency = callback.data.replace('_2', '')
    await callback.answer()
    await callback.message.edit_text(
        f'You chose to convert to {target_currency}. Now, please enter the amount to convert:'
    )

@router.message(F.text)
async def process_amount(message: Message):
    if message.text.isdigit():
        amount = int(message.text)
        await message.answer(f"Thank you! You entered the amount: {amount}")
    else:
        await message.answer("❌ Please enter a valid number (digits only).")

