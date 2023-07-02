import asyncio

from aiogram import Dispatcher

from __init__ import bot
from database import database # Создает, активирует, базу данных
from handler import home, assorts, reviews


# Запуск бота
async def main():
    print('GOAL!')

    dp = Dispatcher()

    dp.include_routers(
        home.route, 
        assorts.route,
        reviews.route)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())