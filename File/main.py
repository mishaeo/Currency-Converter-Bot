import asyncio

from aiogram import Bot, Dispatcher, F
from handlers import router

from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
    bot = Bot(token='7816169467:AAGHjyE1j_BqCDxrFn3quU98mQvoGeHlhYs')
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot is off')